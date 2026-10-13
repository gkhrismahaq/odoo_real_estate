# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class PropertyCatalogController(http.Controller):

    @http.route(
        ["/properties"],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def properties_catalog(self, **kwargs):
        """Menampilkan katalog publik untuk unit properti yang berstatus baru (tersedia)."""
        domain = [
            ("status", "=", "new"),
            ("active", "=", True),
        ]
        properties = (
            request.env["estate.property"]
            .sudo()
            .search(domain, order="id desc")
        )
        values = {
            "properties": properties,
        }
        return request.render("estate_booking.property_catalog", values)
