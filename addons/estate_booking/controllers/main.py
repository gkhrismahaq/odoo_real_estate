# -*- coding: utf-8 -*-

from odoo import fields, http
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

    @http.route(
        ["/property/<int:property_id>"],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def property_detail(self, property_id, **kwargs):
        """Menampilkan rincian informasi unit properti yang berstatus baru (tersedia)."""
        property_sudo = (
            request.env["estate.property"]
            .sudo()
            .browse(property_id)
            .exists()
        )
        if (
            not property_sudo
            or not property_sudo.active
            or property_sudo.status != "new"
        ):
            return request.redirect("/properties")

        values = {
            "property": property_sudo,
        }
        return request.render("estate_booking.property_detail", values)

    @http.route(
        ["/booking/checkout"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def booking_checkout(self, property_id=None, **kwargs):
        """Menampilkan formulir checkout pemesanan unit properti."""
        if not property_id:
            return request.redirect("/properties")
        try:
            prop_id = int(property_id)
        except (ValueError, TypeError):
            return request.redirect("/properties")

        property_sudo = (
            request.env["estate.property"]
            .sudo()
            .browse(prop_id)
            .exists()
        )
        if (
            not property_sudo
            or not property_sudo.active
            or property_sudo.status != "new"
        ):
            return request.redirect("/properties")

        user = request.env.user
        partner = user.partner_id if user and not user._is_public() else None

        values = {
            "property": property_sudo,
            "error": kwargs.get("error"),
            "default_name": kwargs.get("name") or (partner.name if partner else ""),
            "default_email": kwargs.get("email") or (partner.email if partner else ""),
            "default_phone": kwargs.get("phone") or (partner.phone if partner else ""),
        }
        return request.render("estate_booking.booking_checkout", values)

    @http.route(
        ["/booking/checkout/submit"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def booking_checkout_submit(self, **post):
        """Memproses data formulir checkout dan menerbitkan draf dokumen estate.booking."""
        property_id = post.get("property_id")
        try:
            prop_id = int(property_id)
        except (ValueError, TypeError):
            return request.redirect("/properties")

        property_sudo = (
            request.env["estate.property"]
            .sudo()
            .browse(prop_id)
            .exists()
        )
        if (
            not property_sudo
            or not property_sudo.active
            or property_sudo.status != "new"
        ):
            return request.redirect("/properties")

        name = (post.get("name") or "").strip()
        email = (post.get("email") or "").strip().lower()
        phone = (post.get("phone") or "").strip()

        if not name or not email:
            error_msg = "Nama lengkap dan email wajib diisi."
            return request.redirect(
                f"/booking/checkout?property_id={prop_id}&error={error_msg}&name={name}&email={email}&phone={phone}"
            )

        # Kelola kontak pemesan via sudo
        Partner = request.env["res.partner"].sudo()
        partner = Partner.search([("email", "=ilike", email)], limit=1)
        if not partner:
            partner = Partner.create({
                "name": name,
                "email": email,
                "phone": phone,
            })
        else:
            if phone and not partner.phone:
                partner.write({"phone": phone})

        # Penomoran referensi unik reservasi
        count = request.env["estate.booking"].sudo().search_count([]) + 1
        booking_ref = f"BK-{fields.Date.today().strftime('%Y%m%d')}-{count:04d}"

        booking = request.env["estate.booking"].sudo().create({
            "name": booking_ref,
            "property_id": property_sudo.id,
            "customer_id": partner.id,
            "booking_date": fields.Date.today(),
            "booking_fee_paid": property_sudo.booking_fee,
            "currency_id": property_sudo.currency_id.id if property_sudo.currency_id else request.env.company.currency_id.id,
            "state": "draft",
        })

        return request.redirect(f"/booking/confirmation/{booking.id}")

    @http.route(
        ["/booking/confirmation/<int:booking_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def booking_confirmation(self, booking_id, **kwargs):
        """Menampilkan halaman konfirmasi pemesanan sukses."""
        booking_sudo = (
            request.env["estate.booking"]
            .sudo()
            .browse(booking_id)
            .exists()
        )
        if not booking_sudo:
            return request.redirect("/properties")

        values = {
            "booking": booking_sudo,
            "property": booking_sudo.property_id,
            "transaction": booking_sudo.payment_transaction_id,
        }
        return request.render("estate_booking.booking_confirmation", values)

    @http.route(
        ["/booking/pay/<int:booking_id>"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def booking_pay(self, booking_id, provider_id=None, **kwargs):
        """Menyajikan halaman pembayaran uang tanda jadi pemesanan properti."""
        booking_sudo = (
            request.env["estate.booking"]
            .sudo()
            .browse(booking_id)
            .exists()
        )
        if not booking_sudo:
            return request.redirect("/properties")

        # Jika booking sudah terkonfirmasi atau dibatalkan, arahkan ke konfirmasi
        if booking_sudo.state in ("confirmed", "canceled"):
            return request.redirect(f"/booking/confirmation/{booking_sudo.id}")

        selected_provider_id = (
            int(provider_id)
            if provider_id and str(provider_id).isdigit()
            else None
        )

        error_msg = kwargs.get("error")
        tx_sudo = booking_sudo.payment_transaction_id

        # Inisiasi atau ambil payment.transaction via model layer
        try:
            tx_sudo = booking_sudo._create_or_get_payment_transaction(
                provider_id=selected_provider_id
            )
        except Exception as e:
            error_msg = str(e)

        # Ambil penyedia pembayaran aktif untuk disajikan pada template
        providers_sudo = (
            request.env["payment.provider"]
            .sudo()
            .search([
                ("state", "in", ("test", "enabled")),
                ("company_id", "in", [request.env.company.id, False]),
            ], order="state desc, id asc")
        )

        values = {
            "booking": booking_sudo,
            "property": booking_sudo.property_id,
            "transaction": tx_sudo,
            "tx_state": tx_sudo.state if tx_sudo else False,
            "providers": providers_sudo,
            "error": error_msg,
        }
        return request.render("estate_booking.booking_payment", values)

    @http.route(
        ["/booking/pay/simulate/<int:booking_id>"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def booking_pay_simulate(self, booking_id, **post):
        """Memproses simulasi callback notifikasi pembayaran (khusus Test Provider)."""
        booking_sudo = (
            request.env["estate.booking"]
            .sudo()
            .browse(booking_id)
            .exists()
        )
        if not booking_sudo or not booking_sudo.payment_transaction_id:
            return request.redirect("/properties")

        tx_sudo = booking_sudo.payment_transaction_id

        # Simulasikan payload notifikasi callback dari provider
        simulated_data = {
            "reference": tx_sudo.reference,
            "status": "success",
            "simulated": True,
            "simulated_state": "done",
        }

        # Jalankan pemrosesan notifikasi callback pada payment.transaction
        tx_sudo._process_notification_data(simulated_data)

        # Ubah status transaksi menjadi 'done' jika belum diset oleh provider
        if tx_sudo.state != "done":
            if hasattr(tx_sudo, "_set_done"):
                tx_sudo._set_done()
            else:
                tx_sudo.write({"state": "done"})

        return request.redirect(f"/booking/pay/{booking_sudo.id}")



