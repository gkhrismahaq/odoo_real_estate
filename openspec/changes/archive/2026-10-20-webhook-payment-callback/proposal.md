## Why

Setelah pengguna menginisiasi transaksi pembayaran tanda jadi (`payment.transaction`) pada antarmuka checkout pembayaran, sistem memerlukan mekanisme untuk menangkap notifikasi sinyal balik (*webhook* / *callback notification*) dari Payment Gateway (termasuk Test Provider Odoo). Saat ini, transaksi pembayaran baru sampai pada tahap inisiasi draf dan belum memiliki logika penanganan umpan balik notifikasi (`_process_notification_data()`) untuk memvalidasi bahwa transaksi pembayaran telah berstatus sukses (`done`), memverifikasi integritas nominal yang dibayarkan terhadap nilai tagihan uang tanda jadi (`booking_fee_paid`), serta mencatat validasi pembayaran pada rekaman transaksi.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 1.3, 2.2, 3.2, & 3.3.
> **Reference:** [Roadmap](../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

## What Changes

- **Penanganan Notifikasi Pembayaran pada Model Transaksi:**
  - Meng-*override* method `_process_notification_data(self, notification_data)` pada model `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`) untuk memproses data notifikasi dari payment provider, memanggil logika dasar Odoo (`super()`), dan memvalidasi keberhasilan pembayaran untuk transaksi yang terhubung dengan `booking_id`.
  - Melakukan verifikasi konsistensi data antara nominal yang terbayar pada `payment.transaction` dengan nilai `booking_fee_paid` pada dokumen reservasi terkait guna mencegah selisih pembayaran atau manipulasi data.
- **Penyempurnaan Penanganan Status Pembayaran pada Portal:**
  - Memperbarui controller pada `addons/estate_booking/controllers/main.py` untuk menangani umpan balik status transaksi (sukses, pending, atau gagal) saat pengguna kembali dari gerbang pembayaran dan menampilkan informasi status terkini pada portal.
  - Memperbarui template portal pembayaran `addons/estate_booking/views/portal_booking_payment_templates.xml` untuk menyajikan status konfirmasi pembayaran sukses ketika transaksi telah divalidasi oleh sistem.

## Capabilities

### Modified Capabilities
- `payment-gateway-integration`: Penambahan kapabilitas penangkapan notifikasi gateway pembayaran (*webhook callback*) via method `_process_notification_data()` pada `payment.transaction`, validasi keberhasilan status pembayaran uang tanda jadi, dan verifikasi integritas data transaksi.

## Impact

- **Files modified:**
  - `addons/estate_booking/models/payment_transaction.py`
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/views/portal_booking_payment_templates.xml`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 1.3, 2.2, 3.2, 3.3)
  - `docs/01-estate_booking/roadmap.md` (Fase 4, Bagian 4.1)

**Estimated effort:** 2 hours.
