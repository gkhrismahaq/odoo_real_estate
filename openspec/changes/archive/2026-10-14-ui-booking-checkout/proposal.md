## Why

Setelah calon pembeli meninjau spesifikasi unit dan mengklik tombol "Book Now" pada halaman rincian properti, sistem memerlukan antarmuka formulir checkout (`/booking/checkout`) untuk mengumpulkan data identitas pemesan (nama, email, telepon), memvalidasi ketersediaan unit, serta menerbitkan dokumen draf reservasi `estate.booking` sebelum diarahkan ke gerbang pembayaran digital.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.
> **Reference:** [Roadmap](../../docs/01-estate_booking/roadmap.md) — Fase 3, Bagian 3.1.

## What Changes

- Penambahan method controller publik pada `addons/estate_booking/controllers/main.py`:
  - Route GET `/booking/checkout`: Menyajikan halaman formulir identitas pemesan dan ringkasan nilai uang tanda jadi (*booking fee*).
  - Route POST `/booking/checkout/submit`: Memvalidasi data input, mengaitkan/membuat kontak `res.partner`, dan membuat rekaman dokumen baru `estate.booking` dalam status `draft`.
  - Route GET `/booking/confirmation/<int:booking_id>`: Menyajikan halaman konfirmasi pemesanan sukses lengkap dengan nomor referensi booking dan instruksi pelunasan tanda jadi.
- Pembuatan template QWeb `addons/estate_booking/views/portal_booking_checkout_templates.xml` untuk halaman formulir checkout dan halaman konfirmasi pemesanan.
- Pendaftaran berkas template QWeb baru pada deklarasi `data` di `addons/estate_booking/__manifest__.py`.

## Capabilities

### Modified Capabilities
- `portal-property-catalog`: Penambahan alur formulir checkout pemesanan properti (`/booking/checkout`), pembuatan rekaman reservasi `estate.booking`, dan halaman konfirmasi reservasi (`/booking/confirmation/<id>`).

## Impact

- **Files created:**
  - `addons/estate_booking/views/portal_booking_checkout_templates.xml`
- **Files modified:**
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 2.2, 3.2, 3.4)
  - `docs/01-estate_booking/roadmap.md` (Fase 3, Bagian 3.1)

**Estimated effort:** 3 hours.
