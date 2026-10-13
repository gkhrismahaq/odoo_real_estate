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
