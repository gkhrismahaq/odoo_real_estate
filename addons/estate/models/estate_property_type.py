from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Nama Tipe Properti sudah ada"),
    ]

    name = fields.Char(string="Nama", required=True)
    sequence = fields.Integer(string="Urutan", default=1)

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Penawaran",
    )
    offer_count = fields.Integer(
        string="Jumlah Penawaran",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
