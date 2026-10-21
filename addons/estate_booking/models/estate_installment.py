# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EstateInstallment(models.Model):
    _name = "estate.installment"
    _description = "Estate Installment"
    _order = "due_date asc, id asc"

    booking_id = fields.Many2one(
        "estate.booking",
        string="Reservasi",
        required=True,
        ondelete="cascade",
        index=True,
    )
    name = fields.Char(string="Keterangan", required=True)
    due_date = fields.Date(string="Tanggal Jatuh Tempo", required=True)
    currency_id = fields.Many2one(
        "res.currency",
        string="Mata Uang",
        related="booking_id.currency_id",
        store=True,
        readonly=True,
    )
    amount = fields.Monetary(
        string="Nilai Tagihan",
        currency_field="currency_id",
        required=True,
    )
    invoice_id = fields.Many2one(
        "account.move",
        string="Faktur Tagihan",
        readonly=True,
        copy=False,
        index=True,
    )
    state = fields.Selection(
        selection=[
            ("unpaid", "Belum Lunas"),
            ("paid", "Lunas"),
            ("late", "Terlambat"),
        ],
        string="Status",
        compute="_compute_state",
        store=True,
        readonly=False,
        copy=False,
        default="unpaid",
    )

    @api.depends("invoice_id.payment_state", "invoice_id.state", "due_date")
    def _compute_state(self):
        """Menyinkronkan status cicilan secara dinamis berdasarkan status pelunasan faktur
        akuntansi (payment_state) serta tenggat waktu tanggal jatuh tempo.
        """
        today = fields.Date.context_today(self)
        for record in self:
            if record.invoice_id and record.invoice_id.payment_state in ("paid", "in_payment"):
                record.state = "paid"
            elif record.due_date and record.due_date < today:
                record.state = "late"
            else:
                record.state = "unpaid"

    def action_create_invoice(self):
        """Menerbitkan dokumen draf faktur pelanggan (account.move bertipe out_invoice)
        berdasarkan data entitas cicilan pembiayaan.
        """
        AccountMove = self.env["account.move"]
        AccountJournal = self.env["account.journal"]

        for record in self:
            if record.invoice_id:
                raise UserError(
                    _("Faktur untuk cicilan '%s' sudah pernah diterbitkan (Referensi: %s).")
                    % (record.name, record.invoice_id.name or record.invoice_id.id)
                )

            if not record.booking_id:
                raise UserError(_("Cicilan '%s' tidak terhubung dengan dokumen reservasi.") % record.name)

            if not record.booking_id.customer_id:
                raise UserError(
                    _("Dokumen reservasi '%s' tidak memiliki mitra klien pembeli yang valid.")
                    % record.booking_id.name
                )

            if not record.amount or record.amount <= 0:
                raise UserError(
                    _("Nilai tagihan cicilan '%s' harus lebih besar dari 0 untuk membuat faktur.")
                    % record.name
                )

            # Cari Jurnal Penjualan aktif pada perusahaan terkait
            company = record.booking_id.company_id if hasattr(record.booking_id, "company_id") and record.booking_id.company_id else self.env.company
            journal = AccountJournal.search([
                ("type", "=", "sale"),
                ("company_id", "in", [company.id, False]),
            ], limit=1)

            currency = record.currency_id or record.booking_id.currency_id or company.currency_id

            property_name = record.booking_id.property_id.name if record.booking_id.property_id else ""
            line_description = f"{record.booking_id.name} - {record.name}"
            if property_name:
                line_description += f" ({property_name})"

            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": record.booking_id.customer_id.id,
                "currency_id": currency.id,
                "invoice_date": fields.Date.context_today(record),
                "invoice_date_due": record.due_date,
                "ref": f"{record.booking_id.name} - {record.name}",
                "invoice_origin": record.booking_id.name,
                "invoice_line_ids": [
                    (0, 0, {
                        "name": line_description,
                        "quantity": 1.0,
                        "price_unit": record.amount,
                        "currency_id": currency.id,
                    })
                ],
            }
            if journal:
                invoice_vals["journal_id"] = journal.id

            move = AccountMove.create(invoice_vals)
            record.write({"invoice_id": move.id})
            _logger.info(
                "Berhasil menerbitkan draf faktur pelanggan %s untuk cicilan %s (ID: %s).",
                move.name or move.id,
                record.name,
                record.id,
            )

        if len(self) == 1:
            return self.action_view_invoice()
        return True

    def action_view_invoice(self):
        """Membuka tampilan formulir dokumen faktur akuntansi yang terhubung."""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("Cicilan '%s' belum memiliki faktur akuntansi.") % self.name)
        return {
            "name": _("Faktur Tagihan"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.invoice_id.id,
            "target": "current",
        }

    @api.model
    def _cron_generate_due_installment_invoices(self):
        """Memindai dan menerbitkan draf faktur pelanggan secara otomatis untuk
        seluruh cicilan yang telah jatuh tempo (due_date <= context_today) dan belum memiliki faktur.
        """
        today = fields.Date.context_today(self)
        due_installments = self.search([
            ("due_date", "<=", today),
            ("invoice_id", "=", False),
            ("state", "!=", "paid"),
            ("booking_id.state", "=", "confirmed"),
        ])
        _logger.info(
            "Memulai eksekusi cron penagihan cicilan. Ditemukan %s cicilan jatuh tempo tanpa faktur.",
            len(due_installments),
        )
        created_count = 0
        for inst in due_installments:
            try:
                inst.action_create_invoice()
                created_count += 1
            except Exception as e:
                _logger.error(
                    "Gagal membuat faktur otomatis untuk cicilan %s (ID: %s): %s",
                    inst.name,
                    inst.id,
                    str(e),
                )
        _logger.info(
            "Selesai eksekusi cron penagihan cicilan. Berhasil menerbitkan %s draf faktur.",
            created_count,
        )
        return True
