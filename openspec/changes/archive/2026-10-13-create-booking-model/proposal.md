## Why

Model `estate.property` sudah memiliki status reservasi dan biaya pemesanan, tetapi belum ada dokumen reservasi yang menyimpan properti, klien, tanggal transaksi, nilai pembayaran awal, serta status prosesnya. Dokumen tersebut diperlukan sebagai dasar alur pembayaran sebelum integrasi transaksi, perubahan status properti, dan jadwal cicilan dapat dikerjakan pada change berikutnya.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 2, capability `property-booking-models`, change `create-booking-model`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2 dan 3.3.

## What Changes

- Menambahkan model Odoo baru `estate.booking` untuk mencatat dokumen reservasi properti.
- Menyediakan field referensi, relasi properti dan klien, tanggal pemesanan, nilai booking fee yang dibayar, relasi transaksi pembayaran, relasi jadwal cicilan, serta status reservasi.
- Mendefinisikan state `draft`, `waiting_payment`, `confirmed`, dan `canceled` beserta transisi yang menjadi tanggung jawab model ini.
- Menambahkan relasi balik daftar reservasi pada perluasan `estate.property` yang sudah ada.

## Capabilities

### New Capabilities

Tidak ada.

### Modified Capabilities

- `property-booking-models`: Menambahkan kemampuan untuk mencatat dokumen `estate.booking`, relasinya dengan properti dan klien, serta siklus status reservasi.

## Impact

- **Files created:**
  - `addons/estate_booking/models/estate_booking.py`
- **Files modified:**
  - `addons/estate_booking/models/__init__.py`
  - `addons/estate_booking/models/estate_property.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 4 hours.
