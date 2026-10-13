## Why

Agen properti memerlukan antarmuka grafis di backend Odoo untuk mengelola, meninjau, dan memantau dokumen reservasi (`estate.booking`) beserta jadwal pembiayaan/cicilan (`estate.installment`) secara visual melalui tampilan List/Tree, Form, dan Search filter, serta kemudahan navigasi melalui struktur menu di bawah modul manajemen properti.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

## What Changes

- Pembuatan tampilan Tree (List), Form, Search filter, dan Window Action untuk model `estate.booking`.
- Pada form reservasi, penambahan header berisi tombol status action (`action_waiting_payment`, `action_confirm`, `action_cancel`) dan widget statusbar.
- Pada form reservasi, penyematan inline list view untuk relasi `installment_ids`.
- Pembuatan tampilan Tree (List), Form, Search filter, dan Window Action untuk model `estate.installment`.
- Pembuatan struktur menu backend baru di bawah root menu `estate.estate_property_root` ("Manajemen Properti") yang memuat submenu untuk Reservasi dan Jadwal Cicilan.
- Pendaftaran file XML views dan menus baru ke dalam deklarasi `data` pada `addons/estate_booking/__manifest__.py`.

## Capabilities

### Modified Capabilities
- `property-booking-models`: Penambahan kebutuhan antarmuka backend (Tree/List, Form, Search filter) dan navigasi menu bagi pengguna internal untuk model reservasi properti dan jadwal cicilan pembiayaan.

## Impact

- **Files created:**
  - `addons/estate_booking/views/estate_booking_views.xml`
  - `addons/estate_booking/views/estate_installment_views.xml`
  - `addons/estate_booking/views/estate_booking_menus.xml`
- **Files modified:**
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 3.4)
  - `docs/01-estate_booking/roadmap.md` (Bagian 2.1)

**Estimated effort:** 3 hours.
