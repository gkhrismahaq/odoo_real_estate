from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Nama Label Properti sudah ada"),
    ]

    name = fields.Char(string="Nama", required=True)
    color = fields.Integer(string="Warna")
