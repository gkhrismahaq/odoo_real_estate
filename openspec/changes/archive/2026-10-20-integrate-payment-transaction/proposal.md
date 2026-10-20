## Why

Setelah calon pembeli menyelesaikan pengisian formulir checkout dan mendapatkan draf reservasi unit properti (`estate.booking`), sistem memerlukan mekanisme pembayaran digital terintegrasi untuk melunasi uang tanda jadi (*booking fee*). Saat ini, dokumen reservasi baru diterbitkan dalam status `draft` tanpa adanya inisiasi transaksi pembayaran resmi pada modul `payment` Odoo. Sistem memerlukan integrasi dengan arsitektur transaksi pembayaran Odoo (*Payment Engine*, khususnya Test Provider) guna menghasilkan referensi transaksi `payment.transaction`, mengaitkannya ke dokumen reservasi terkait, mengalihkan status reservasi menjadi `waiting_payment`, serta mengarahkan pembeli ke antarmuka pemrosesan pembayaran secara aman.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 1.3, 2.2, 3.1, 3.2, & 3.3.
> **Reference:** [Roadmap](../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

## What Changes

- **Perluasan Model Transaksi Pembayaran:**
  - Menambahkan model ekstensi `payment.transaction` pada `addons/estate_booking/models/payment_transaction.py` dengan penambahan field relasi `booking_id = fields.Many2one("estate.booking")` guna menghubungkan transaksi pembayaran secara dua arah dengan dokumen reservasi properti sesuai arsitektur standar Odoo.
- **Peningkatan Model Reservasi Properti:**
  - Menambahkan method bisnis `action_create_payment_transaction(provider_id=None)` pada model `estate.booking` (`addons/estate_booking/models/estate_booking.py`) untuk menghasilkan atau mengambil referensi `payment.transaction` yang valid dengan nilai nominal sesuai `booking_fee_paid` dan mata uang yang bersesuaian, serta mengalihkan status reservasi dari `draft` ke `waiting_payment`.
- **Pengembangan Controller Rute Pembayaran:**
  - Menambahkan rute GET `/booking/pay/<int:booking_id>` pada `addons/estate_booking/controllers/main.py` untuk memvalidasi status reservasi, menginisiasi transaksi pembayaran atau menyiapkan parameter form pembayaran Odoo, dan menyajikan halaman checkout pembayaran kepada pengguna.
- **Penyempurnaan Antarmuka QWeb Portal:**
  - Menambahkan tombol aksi "Lanjutkan ke Pembayaran" pada template konfirmasi reservasi (`addons/estate_booking/views/portal_booking_checkout_templates.xml`) yang mengarahkan pengguna langsung ke rute `/booking/pay/<booking_id>`.
  - Membuat berkas template QWeb baru `addons/estate_booking/views/portal_booking_payment_templates.xml` yang menyajikan ringkasan tagihan uang tanda jadi dan mengintegrasikan form pembayaran provider Odoo (*payment processing form*).
- **Konfigurasi Modul & Manifest:**
  - Mendaftarkan berkas model baru pada `addons/estate_booking/models/__init__.py`.
  - Mendaftarkan berkas template view baru pada elemen `data` di `addons/estate_booking/__manifest__.py`.

## Capabilities

### New Capabilities
- `payment-gateway-integration`: Menghubungkan proses pemesanan properti (`estate.booking`) dengan mesin transaksi pembayaran Odoo (`payment.transaction`), menginisiasi transaksi pembayaran uang tanda jadi saat proses booking dilanjutkan, mengalihkan status reservasi menjadi `waiting_payment`, dan menyajikan antarmuka pembayaran digital melalui Payment Provider Odoo (Test Provider).

### Modified Capabilities

## Impact

- **Files created:**
  - `addons/estate_booking/models/payment_transaction.py`
  - `addons/estate_booking/views/portal_booking_payment_templates.xml`
- **Files modified:**
  - `addons/estate_booking/models/__init__.py`
  - `addons/estate_booking/models/estate_booking.py`
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/views/portal_booking_checkout_templates.xml`
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 1.3, 2.2, 3.1, 3.2, 3.3)
  - `docs/01-estate_booking/roadmap.md` (Fase 4, Bagian 4.1)

**Estimated effort:** 3 hours.
