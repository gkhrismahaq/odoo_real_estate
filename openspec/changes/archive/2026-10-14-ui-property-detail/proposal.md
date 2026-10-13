## Why

Setelah melihat kartu properti pada halaman katalog, calon pembeli membutuhkan halaman rincian unit (`/property/<id>`) untuk meninjau spesifikasi menyeluruh (deskripsi lengkap, luas bangunan & taman, fasilitas garasi, orientasi fasad/taman, tanggal ketersediaan, nilai uang tanda jadi/booking fee) serta tombol aksi "Book Now" untuk melanjutkan ke alur pemesanan.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 2.2.

## What Changes

- Penambahan method controller dengan route publik `/property/<model("estate.property"):property>` pada `addons/estate_booking/controllers/main.py` (`auth='public'`, `website=True`).
- Pengecekan aksesibilitas: membatasi akses detail hanya pada properti yang berstatus `new` dan aktif; jika tidak memenuhi syarat, diarahkan kembali ke katalog `/properties` dengan pesan informasi.
- Pembuatan template QWeb `addons/estate_booking/views/portal_property_detail_templates.xml` yang mewarisi `website.layout`, menyajikan breadcrumb navigasi, kartu hero harga & booking fee, tabel spesifikasi teknis unit, deskripsi lengkap, dan tombol aksi "Book Now".
- Pendaftaran berkas template QWeb baru pada deklarasi `data` di `addons/estate_booking/__manifest__.py`.

## Capabilities

### Modified Capabilities
- `portal-property-catalog`: Penambahan spesifikasi antarmuka detail unit properti publik (`/property/<id>`) dengan rincian spesifikasi lengkap dan tombol inisiasi pemesanan ("Book Now").

## Impact

- **Files created:**
  - `addons/estate_booking/views/portal_property_detail_templates.xml`
- **Files modified:**
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 2.2, 3.2, 3.4)
  - `docs/01-estate_booking/roadmap.md` (Fase 3, Bagian 3.1)

**Estimated effort:** 3 hours.
