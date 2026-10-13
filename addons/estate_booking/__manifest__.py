# -*- coding: utf-8 -*-
{
    "name": "Estate Booking",
    "version": "1.0",
    "summary": "Property Management & E-Commerce Integration System",
    "description": """
        Modul Estate Booking untuk integrasi antara modul estate, website, payment, dan account.
        Memfasilitasi klien untuk memesan properti dan melunasi cicilan.
    """,
    "author": "Gilang Khrismahaq",
    "category": "Sales",
    "depends": [
        "estate",
        "website",
        "payment",
        "account",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_booking_views.xml",
        "views/estate_installment_views.xml",
        "views/estate_booking_menus.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
