# -*- coding: utf-8 -*-

from odoo import fields, models


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
        required=True,
        copy=False,
        default="unpaid",
    )
