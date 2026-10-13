# -*- coding: utf-8 -*-

from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    booking_fee = fields.Float(string="Biaya Pemesanan")
    status = fields.Selection(
        selection_add=[("reserved", "Dipesan")],
        ondelete={"reserved": "set default"},
    )
    booking_ids = fields.One2many(
        "estate.booking",
        "property_id",
        string="Daftar Reservasi",
    )
