# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError


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

    def action_confirm(self):
        for record in self:
            if record.state != "waiting_payment":
                raise UserError(
                    _("Hanya reservasi berstatus Menunggu Pembayaran yang dapat dikonfirmasi.")
                )
            record.state = "confirmed"
        return True

    def action_cancel(self):
        for record in self:
            if record.state != "confirmed":
                raise UserError(
                    _("Hanya reservasi berstatus Terkonfirmasi yang dapat dibatalkan.")
                )
            record.state = "canceled"
        return True
