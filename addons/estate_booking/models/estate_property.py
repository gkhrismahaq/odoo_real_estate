# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.misc import formatLang


class EstateProperty(models.Model):
    _inherit = "estate.property"

    currency_id = fields.Many2one(
        "res.currency",
        string="Mata Uang",
        default=lambda self: self.env.company.currency_id,
    )
    booking_fee = fields.Monetary(
        string="Uang Tanda Jadi (Booking Fee)",
        currency_field="currency_id",
        compute="_compute_booking_fee",
        store=True,
        readonly=False,
        precompute=True,
        help="Nilai tanda jadi untuk mengunci unit. Otomatis terhitung 1% dari Harga Bukaan jika tidak diisi manual.",
    )
    booking_fee_preview = fields.Char(
        string="Pratinjau Uang Tanda Jadi",
        compute="_compute_booking_fee_preview",
        help="Informasi kalkulasi Uang Tanda Jadi untuk admin.",
    )
    status = fields.Selection(
        selection_add=[("reserved", "Dipesan")],
        ondelete={"reserved": "set default"},
    )
    booking_ids = fields.One2many(
        "estate.booking",
        "property_id",
        string="Daftar Reservasi",
    )

    @api.depends("expected_price")
    def _compute_booking_fee(self):
        """Menghitung otomatis 1% dari Harga Bukaan jika belum diisi manual."""
        for record in self:
            if not record.booking_fee and record.expected_price:
                record.booking_fee = record.expected_price * 0.01
            elif not record.booking_fee:
                record.booking_fee = 0.0

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        """Memberikan feedback instan di form saat admin mengetik Harga Bukaan."""
        if self.expected_price and not self.booking_fee:
            self.booking_fee = self.expected_price * 0.01

    @api.depends("expected_price", "booking_fee", "currency_id")
    def _compute_booking_fee_preview(self):
        """Menampilkan teks pratinjau nominal terformat dan persentase untuk admin."""
        for record in self:
            if record.booking_fee and record.expected_price:
                pct = (record.booking_fee / record.expected_price) * 100
                curr = record.currency_id or record.env.company.currency_id
                formatted_fee = formatLang(record.env, record.booking_fee, currency_obj=curr)
                is_one_pct = abs(pct - 1.0) < 0.01
                status_text = "Otomatis 1%" if is_one_pct else f"Manual ({pct:.1f}%)"
                record.booking_fee_preview = f"{status_text} → {formatted_fee}"
            elif record.expected_price:
                est_fee = record.expected_price * 0.01
                curr = record.currency_id or record.env.company.currency_id
                formatted_est = formatLang(record.env, est_fee, currency_obj=curr)
                record.booking_fee_preview = f"Otomatis 1% → {formatted_est}"
            else:
                record.booking_fee_preview = "Ketik Harga Bukaan untuk kalkulasi otomatis 1%."
