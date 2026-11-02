from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Nama Tipe Properti sudah ada"),
    ]

    name = fields.Char(string="Nama", required=True)
    sequence = fields.Integer(string="Urutan", default=1)
