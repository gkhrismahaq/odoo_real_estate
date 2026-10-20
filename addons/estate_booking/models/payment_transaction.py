# -*- coding: utf-8 -*-

from odoo import fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    booking_id = fields.Many2one(
        "estate.booking",
        string="Estate Booking",
        readonly=True,
        index=True,
        copy=False,
        help="Dokumen pemesanan properti yang terkait dengan transaksi pembayaran ini.",
    )
