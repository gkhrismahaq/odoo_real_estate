from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    status = fields.Selection(
        ...,
        tracking=True,
    )
    _order = "id desc"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Harga Bukaan harus lebih dari 0",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Harga Jual harus angka positif atau 0",
        ),
    ]

    name = fields.Char(string="Nama", required=True)
    description = fields.Text(string="Deskripsi")
    postcode = fields.Char(string="Kode Pos")
    date_availability = fields.Date(
        string="Tanggal Tersedia",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Harga Bukaan", required=True)
    selling_price = fields.Float(string="Harga Jual", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Kamar Tidur", default=2)
    living_area = fields.Integer(string="Luas Bangunan")
    facades = fields.Integer(string="Fasad")
    garage = fields.Boolean(string="Garasi")
    garden = fields.Boolean(string="Taman")
    garden_area = fields.Integer(string="Luas Taman")
    garden_orientation = fields.Selection(
        selection=[
            ("south", "Selatan"),
            ("east", "Timur"),
            ("north", "Utara"),
            ("west", "Barat"),
        ],
        string="Orientasi Taman",
        default="north",
    )
    active = fields.Boolean(string="Aktif", default=False)
    status = fields.Selection(
        selection=[
            ("new", "Baru"),
            ("offer_received", "Penawaran Diterima"),
            ("offer_accepted", "Penawaran Disetujui"),
            ("sold", "Terjual"),
            ("canceled", "Dibatalkan"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Tipe Properti")
    salesperson_id = fields.Many2one(
        "res.users", string="Pramuniaga", index=True, default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Pembeli", index=True, copy=False)
    tags_ids = fields.Many2many("estate.property.tags", string="Label Properti")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Penawaran"
    )
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Penawaran Terbaik")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = sum([record.living_area, record.garden_area])

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
                return {
                    "warning": {
                        "title": "Info",
                        "message": "Luas Taman dan Orientasi Taman akan terisi otomatis",
                    }
                }
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.status == "canceled":
                raise UserError("Properti yang sudah dibatalkan tidak bisa terjual")
            record.status = "sold"
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            ninety_percent_expected = record.expected_price * 0.90

            if (
                float_compare(
                    record.selling_price, ninety_percent_expected, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    "Harga Jual tidak boleh lebih rendah dari 90% Harga Bukaan"
                )

    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Properti yang sudah terjual tidak bisa dibatalkan")
            record.status = "canceled"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.status not in ("new", "canceled"):
                raise UserError(
                    "Anda hanya dapat menghapus properti yang berstatus 'Baru' atau 'Dibatalkan'"
                )
