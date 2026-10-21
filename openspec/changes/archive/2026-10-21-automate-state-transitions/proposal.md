## Why

Setelah transaksi pembayaran uang tanda jadi berhasil divalidasi oleh Payment Gateway (berstatus `done`), sistem saat ini belum secara otomatis mengalihkan status dokumen pemesanan dan mengunci ketersediaan unit properti. Sesuai SSOT TSD (Bagian 2.2 alur #4 & Bagian 3.3), sistem harus secara otomatis mengubah status reservasi `estate.booking` dari `waiting_payment` menjadi `confirmed`, serta memperbarui status unit properti `estate.property` dari `new` menjadi `reserved` (Dipesan) sesaat setelah sinyal pelunasan pembayaran terverifikasi sah. Hal ini krusial untuk mencegah unit properti dipesan ganda oleh pengguna lain pada katalog publik.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 2.2, 3.2, & 3.3.
> **Reference:** [Roadmap](../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

## What Changes

- **Otomatisasi Transisi Status pada Model Reservasi (`estate.booking`):**
  - Menyempurnakan method `action_confirm()` pada `estate.booking` agar selain mengalihkan status booking menjadi `confirmed`, juga secara otomatis mengubah status unit properti terkait (`property_id.status = 'reserved'`).
  - Menyempurnakan method `action_cancel()` agar ketika booking dibatalkan, sistem mengembalikan status properti menjadi `new` apabila tidak ada dokumen booking aktif terkonfirmasi lainnya pada properti tersebut.
- **Pemicu Otomatis Pasca-Validasi Transaksi (`payment.transaction`):**
  - Mengintegrasikan pemanggilan otomatis `booking.action_confirm()` pada saat transaksi pembayaran bertransisi atau divalidasi ke status `done` pada method pemrosesan notifikasi callback (`_process_notification_data`).
- **Penyelarasan Status Antarmuka Portal Web:**
  - Memperbarui controller `addons/estate_booking/controllers/main.py` dan template `portal_booking_checkout_templates.xml` agar halaman konfirmasi menyajikan status pemesanan terkonfirmasi dan unit berhasil dipesan secara real-time setelah pembayaran lunas.

## Capabilities

### Modified Capabilities
- `payment-gateway-integration`: Penambahan otomatisasi pengalihan status dokumen reservasi `estate.booking` ke `confirmed` dan status unit properti `estate.property` ke `reserved` secara reaktif sesaat setelah transaksi pembayaran dinyatakan sukses (`done`).

## Impact

- **Files modified:**
  - `addons/estate_booking/models/estate_booking.py`
  - `addons/estate_booking/models/payment_transaction.py`
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/views/portal_booking_checkout_templates.xml`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 2.2, 3.2, 3.3)
  - `docs/01-estate_booking/roadmap.md` (Fase 4, Bagian 4.1)

**Estimated effort:** 2 hours.
