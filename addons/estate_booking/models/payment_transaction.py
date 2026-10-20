# -*- coding: utf-8 -*-

import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    booking_id = fields.Many2one(
        "estate.booking",
        string="Estate Booking",
        readonly=True,
        index=True,
        copy=False,
        help="Dokumen pemesanan properti yang terkait dengan transaksi pembayaran ini.",
    )

    def _process_notification_data(self, notification_data):
        """Memproses data notifikasi umpan balik (webhook/callback) dari penyedia pembayaran
        dan memvalidasi integritas data transaksi pemesanan properti.
        """
        # Dukungan parameter simulated_state untuk Odoo Demo/Test Provider
        if isinstance(notification_data, dict) and getattr(self, "provider_code", None) == "demo":
            notification_data.setdefault("simulated_state", "done")

        super()._process_notification_data(notification_data)

        for tx in self:
            if not tx.booking_id:
                continue

            booking = tx.booking_id
            expected_amount = booking.booking_fee_paid
            expected_currency = booking.currency_id or tx.company_id.currency_id

            # Validasi integritas nominal dan mata uang pembayaran
            if tx.currency_id and expected_currency and tx.currency_id != expected_currency:
                err_msg = _(
                    "Mata uang transaksi pembayaran (%s) tidak cocok dengan mata uang reservasi (%s).",
                    tx.currency_id.name,
                    expected_currency.name,
                )
                _logger.warning(
                    "Anomali pembayaran pada booking %s: %s", booking.name, err_msg
                )
                if hasattr(tx, "_set_error"):
                    tx._set_error(err_msg)
                else:
                    tx.write({"state": "error", "state_message": err_msg})
                continue

            if tx.amount and expected_amount and tx.amount < expected_amount:
                err_msg = _(
                    "Nominal transaksi pembayaran (%s) kurang dari tagihan uang tanda jadi (%s).",
                    tx.amount,
                    expected_amount,
                )
                _logger.warning(
                    "Anomali pembayaran pada booking %s: %s", booking.name, err_msg
                )
                if hasattr(tx, "_set_error"):
                    tx._set_error(err_msg)
                else:
                    tx.write({"state": "error", "state_message": err_msg})
                continue

            _logger.info(
                "Notifikasi pembayaran untuk booking %s berhasil diproses. Referensi Tx: %s, Status: %s",
                booking.name,
                tx.reference,
                tx.state,
            )

