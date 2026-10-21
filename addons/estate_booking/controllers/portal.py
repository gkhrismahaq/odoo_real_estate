# -*- coding: utf-8 -*-

import logging

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

_logger = logging.getLogger(__name__)


class EstateBookingCustomerPortal(CustomerPortal):
    """Controller ekstensi portal pelanggan Odoo untuk menyajikan data reservasi properti,

    jadwal termin cicilan pembiayaan, dan navigasi langsung ke faktur pembayaran.
    """

    def _prepare_home_portal_values(self, counters):
        """Menyuntikkan counter jumlah reservasi properti milik mitra login ke beranda portal."""
        values = super()._prepare_home_portal_values(counters)
        if "booking_count" in counters:
            partner = request.env.user.partner_id
            booking_model = request.env["estate.booking"]
            values["booking_count"] = (
                booking_model.search_count([("customer_id", "=", partner.id)])
                if booking_model.check_access_rights("read", raise_exception=False)
                else 0
            )
        return values

    @http.route(
        ["/my/bookings", "/my/bookings/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_bookings(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        """Menampilkan daftar riwayat pemesanan unit properti milik pengguna portal."""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        booking_model = request.env["estate.booking"]

        domain = [("customer_id", "=", partner.id)]

        searchbar_sortings = {
            "date": {
                "label": _("Tanggal Terbaru"),
                "order": "booking_date desc, id desc",
            },
            "name": {"label": _("Nomor Referensi"), "order": "name asc"},
            "status": {"label": _("Status"), "order": "state asc, id desc"},
        }
        if not sortby or sortby not in searchbar_sortings:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        booking_count = booking_model.search_count(domain)
        items_per_page = getattr(self, "_items_per_page", 20)
        pager = portal_pager(
            url="/my/bookings",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
            },
            total=booking_count,
            page=page,
            step=items_per_page,
        )

        bookings = booking_model.search(
            domain,
            order=order,
            limit=items_per_page,
            offset=pager["offset"],
        )

        values.update(
            {
                "date": date_begin,
                "bookings": bookings,
                "page_name": "booking",
                "pager": pager,
                "default_url": "/my/bookings",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("estate_booking.portal_my_bookings", values)

    @http.route(
        ["/my/bookings/<int:booking_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_booking_detail(
        self, booking_id=None, access_token=None, **kw
    ):
        """Menyajikan halaman rincian reservasi properti, informasi unit, uang tanda jadi,

        serta tabel jadwal termin cicilan pembiayaan beserta tautan faktur.
        Menerapkan pencegahan akses lintas pengguna (Anti-IDOR).
        """
        partner = request.env.user.partner_id
        try:
            booking = request.env["estate.booking"].sudo().browse(booking_id)
            if not booking.exists() or booking.customer_id.id != partner.id:
                _logger.warning(
                    "Akses ditolak (IDOR protection): Partner %s mencoba mengakses booking %s milik partner %s",
                    partner.id,
                    booking_id,
                    booking.customer_id.id if booking.exists() else "None",
                )
                return request.redirect("/my/bookings")
        except (AccessError, MissingError):
            return request.redirect("/my/bookings")

        values = {
            "booking": booking,
            "page_name": "booking_detail",
        }
        values = self._get_page_view_values(
            booking, access_token, values, "my_bookings_history", False, **kw
        )
        return request.render("estate_booking.portal_my_booking_detail", values)
