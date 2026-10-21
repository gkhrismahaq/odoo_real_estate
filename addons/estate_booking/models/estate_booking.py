# -*- coding: utf-8 -*-

import logging
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class EstateBooking(models.Model):
    _name = "estate.booking"
    _description = "Estate Booking"
    _order = "id desc"

    name = fields.Char(string="Nomor Referensi", required=True, copy=False)
    property_id = fields.Many2one(
        "estate.property",
        string="Properti",
        required=True,
        index=True,
    )
    customer_id = fields.Many2one(
        "res.partner",
        string="Klien",
        required=True,
        index=True,
    )
    booking_date = fields.Date(
        string="Tanggal Transaksi",
        default=fields.Date.context_today,
        copy=False,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Mata Uang",
        default=lambda self: self.env.company.currency_id,
    )
    booking_fee_paid = fields.Monetary(
        string="Nilai Pembayaran Awal",
        currency_field="currency_id",
    )
    installment_term = fields.Integer(
        string="Termin Cicilan (Bulan)",
        default=12,
        required=True,
        help="Jumlah termin pembayaran cicilan berkala dalam satuan bulan.",
    )
    remaining_amount = fields.Monetary(
        string="Sisa Kewajiban Pembayaran",
        currency_field="currency_id",
        compute="_compute_remaining_amount",
        store=True,
        help="Sisa nilai pokok properti yang harus dilunasi melalui cicilan berkala.",
    )
    payment_transaction_id = fields.Many2one(
        "payment.transaction",
        string="Transaksi Pembayaran",
        copy=False,
    )
    installment_ids = fields.One2many(
        "estate.installment",
        "booking_id",
        string="Jadwal Pembiayaan",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("waiting_payment", "Menunggu Pembayaran"),
            ("confirmed", "Terkonfirmasi"),
            ("canceled", "Dibatalkan"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="draft",
    )

    @api.depends("property_id.selling_price", "property_id.expected_price", "booking_fee_paid")
    def _compute_remaining_amount(self):
        for record in self:
            total_price = 0.0
            if record.property_id:
                total_price = record.property_id.selling_price or record.property_id.expected_price or 0.0
            record.remaining_amount = max(0.0, total_price - (record.booking_fee_paid or 0.0))

    @api.constrains("installment_term", "booking_fee_paid", "property_id")
    def _check_installment_and_booking_fee(self):
        for record in self:
            if record.installment_term <= 0:
                raise ValidationError(_("Jumlah termin cicilan harus lebih besar dari 0."))
            if record.property_id:
                total_price = record.property_id.selling_price or record.property_id.expected_price or 0.0
                if record.booking_fee_paid and total_price > 0 and record.booking_fee_paid > total_price:
                    raise ValidationError(
                        _("Nilai uang tanda jadi (%s) tidak boleh melebihi total harga properti (%s).")
                        % (record.booking_fee_paid, total_price)
                    )

    def action_waiting_payment(self):
        for record in self:
            if record.state != "draft":
                raise UserError(
                    _("Hanya reservasi berstatus Draft yang dapat dialihkan ke Menunggu Pembayaran.")
                )
            record.state = "waiting_payment"
        return True

    def _create_or_get_payment_transaction(self, provider_id=None):
        """Menginisiasi atau mengambil rekaman transaksi pembayaran payment.transaction
        untuk pelunasan uang tanda jadi (booking fee).
        """
        self.ensure_one()

        if self.state not in ("draft", "waiting_payment"):
            raise UserError(
                _("Transaksi pembayaran hanya dapat diproses untuk reservasi berstatus Draft atau Menunggu Pembayaran.")
            )

        if not self.booking_fee_paid or self.booking_fee_paid <= 0:
            raise UserError(
                _("Nilai uang tanda jadi (booking fee) harus lebih besar dari 0 untuk memproses transaksi.")
            )

        PaymentTransaction = self.env["payment.transaction"].sudo()

        # Idempotency: Gunakan transaksi yang sudah ada jika belum selesai (bukan cancel / error)
        existing_tx = PaymentTransaction.search([
            ("booking_id", "=", self.id),
            ("state", "not in", ["cancel", "error"]),
        ], order="id desc", limit=1)

        if existing_tx:
            if not self.payment_transaction_id or self.payment_transaction_id != existing_tx:
                self.write({"payment_transaction_id": existing_tx.id})
            if self.state == "draft":
                self.action_waiting_payment()
            return existing_tx

        # Cari Payment Provider yang aktif
        PaymentProvider = self.env["payment.provider"].sudo()
        if provider_id:
            provider = PaymentProvider.browse(provider_id).exists()
            if not provider or provider.state not in ("test", "enabled"):
                raise UserError(_("Penyedia pembayaran yang dipilih tidak valid atau tidak aktif."))
        else:
            # Prioritaskan Test provider atau provider pertama yang aktif
            provider = PaymentProvider.search([
                ("state", "in", ("test", "enabled")),
                ("company_id", "in", [self.env.company.id, False]),
            ], order="state desc, id asc", limit=1)

            if not provider:
                raise UserError(_("Tidak ditemukan penyedia pembayaran (Payment Provider) yang aktif pada sistem."))

        # Referensi unik transaksi
        reference = f"{self.name}-PAY-{fields.Datetime.now().strftime('%Y%m%d%H%M%S')}"
        currency = self.currency_id or self.env.company.currency_id

        tx_values = {
            "provider_id": provider.id,
            "reference": reference,
            "amount": self.booking_fee_paid,
            "currency_id": currency.id,
            "partner_id": self.customer_id.id,
            "operation": "online_redirect",
            "booking_id": self.id,
            "state": "draft",
        }

        # Dukung payment_method_id jika tersedia pada modul payment Odoo 17
        if hasattr(provider, "payment_method_ids") and provider.payment_method_ids:
            tx_values["payment_method_id"] = provider.payment_method_ids[0].id

        tx = PaymentTransaction.create(tx_values)
        self.write({"payment_transaction_id": tx.id})

        if self.state == "draft":
            self.action_waiting_payment()

        return tx

    def action_generate_installments(self):
        """Membentuk deretan baris jadwal cicilan (estate.installment) berdasarkan
        sisa kewajiban pembayaran (remaining_amount) dan jumlah termin (installment_term).
        """
        for record in self:
            if record.installment_term <= 0:
                raise UserError(_("Jumlah termin cicilan harus lebih besar dari 0."))

            # Proteksi integritas data: Larang regenerasi jika sudah ada cicilan yang memiliki faktur atau lunas
            existing_invoiced = record.installment_ids.filtered(
                lambda inst: bool(inst.invoice_id) or inst.state == "paid"
            )
            if existing_invoiced:
                raise UserError(
                    _(
                        "Jadwal cicilan tidak dapat dibuat ulang karena sebagian cicilan sudah memiliki faktur akuntansi atau telah berstatus lunas."
                    )
                )

            # Jika sisa kewajiban 0 atau tidak ada, bersihkan cicilan lama yang belum berfaktur
            if not record.remaining_amount or record.remaining_amount <= 0:
                if record.installment_ids:
                    record.installment_ids.unlink()
                _logger.info(
                    "Sisa kewajiban booking %s bernilai 0. Tidak ada jadwal cicilan yang dibuat.",
                    record.name,
                )
                continue

            # Bersihkan cicilan lama yang belum berfaktur sebelum regenerasi
            if record.installment_ids:
                record.installment_ids.unlink()

            currency = record.currency_id or self.env.company.currency_id
            term_count = record.installment_term
            total_remaining = record.remaining_amount

            # Hitung nominal dasar per termin dibulatkan ke presisi mata uang
            base_amount = currency.round(total_remaining / term_count)
            start_date = record.booking_date or fields.Date.context_today(record)

            installment_vals_list = []
            accumulated_amount = 0.0

            for i in range(1, term_count + 1):
                due_date = start_date + relativedelta(months=i)
                if i == term_count:
                    # Penyesuaian selisih pembulatan pada termin terakhir
                    amount = currency.round(total_remaining - accumulated_amount)
                else:
                    amount = base_amount
                    accumulated_amount += amount

                installment_vals_list.append({
                    "booking_id": record.id,
                    "name": f"{record.name} - Cicilan {i}/{term_count}",
                    "due_date": due_date,
                    "amount": amount,
                    "state": "unpaid",
                })

            self.env["estate.installment"].create(installment_vals_list)
            _logger.info(
                "Berhasil membuat %s baris jadwal cicilan untuk booking %s dengan total nilai %s.",
                term_count,
                record.name,
                total_remaining,
            )
        return True

    def action_confirm(self):
        for record in self:
            if record.state == "confirmed":
                # Idempotency: Jika reservasi sudah confirmed, pastikan unit properti tetap berstatus reserved
                if record.property_id and record.property_id.status != "reserved":
                    record.property_id.status = "reserved"
                if not record.installment_ids and record.remaining_amount > 0:
                    record.action_generate_installments()
                continue

            if record.state != "waiting_payment":
                raise UserError(
                    _("Hanya reservasi berstatus Menunggu Pembayaran yang dapat dikonfirmasi.")
                )

            # Validasi ketersediaan unit properti sebelum mengunci status
            if record.property_id:
                if record.property_id.status in ("sold", "canceled"):
                    raise UserError(
                        _("Unit properti '%s' tidak dapat dipesan karena berstatus '%s'.")
                        % (record.property_id.name, record.property_id.status)
                    )
                record.property_id.status = "reserved"

            record.state = "confirmed"
            _logger.info(
                "Reservasi %s berhasil dikonfirmasi. Unit properti %s beralih ke status 'reserved'.",
                record.name,
                record.property_id.name if record.property_id else "-",
            )

            # Otomatisasi pembentukan draf jadwal cicilan pasca-konfirmasi
            if not record.installment_ids and record.remaining_amount > 0:
                record.action_generate_installments()
        return True

    def action_cancel(self):
        for record in self:
            if record.state != "confirmed":
                raise UserError(
                    _("Hanya reservasi berstatus Terkonfirmasi yang dapat dibatalkan.")
                )
            record.state = "canceled"
            _logger.info("Reservasi %s telah dibatalkan.", record.name)

            if record.property_id:
                # Verifikasi apakah terdapat reservasi terkonfirmasi aktif lainnya untuk unit ini
                other_confirmed_count = self.search_count([
                    ("id", "!=", record.id),
                    ("property_id", "=", record.property_id.id),
                    ("state", "=", "confirmed"),
                ])
                if other_confirmed_count == 0 and record.property_id.status == "reserved":
                    record.property_id.status = "new"
                    _logger.info(
                        "Status unit properti %s dikembalikan menjadi 'new' karena tidak ada reservasi aktif lainnya.",
                        record.property_id.name,
                    )
        return True
