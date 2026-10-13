## Why

Model `estate.booking` dan `estate.installment` telah dibuat pada sistem, namun belum memiliki konfigurasi hak akses model (`ir.model.access.csv`) dan aturan rekaman (`security.xml`). Ketiadaan konfigurasi keamanan ini menyebabkan peringatan hak akses pada Odoo serta tidak terpenuhinya prinsip isolasi data, di mana klien portal berisiko tidak dapat melihat dokumen reservasi miliknya atau sebaliknya melihat dokumen milik klien lain. Konfigurasi keamanan ini diperlukan untuk memastikan Agen Properti memiliki hak CRUD penuh, Klien Portal hanya dapat membaca data miliknya sendiri, dan Pengunjung Publik tidak memiliki akses ke data internal.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 2, capability `property-booking-models`, change `setup-booking-security`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

## What Changes

- Menambahkan direktori `addons/estate_booking/security/` beserta file hak akses `ir.model.access.csv` untuk model `estate.booking` dan `estate.installment`.
- Mengatur hak akses Agen Properti (grup internal `base.group_user`) dengan izin penuh membaca, membuat, mengubah, dan menghapus (CRUD: `1,1,1,1`).
- Mengatur hak akses Klien Portal (grup portal `base.group_portal`) dengan izin membaca (Read: `1,0,0,0`).
- Menambahkan file `addons/estate_booking/security/security.xml` yang memuat record rules (`ir.rule`) multi-tenant agar Klien Portal hanya dapat membaca dokumen reservasi dan cicilan yang terhubung dengan akun mereka sendiri.
- Memperbarui `addons/estate_booking/__manifest__.py` dengan mendaftarkan file `security/security.xml` dan `security/ir.model.access.csv` ke dalam daftar `data`.

## Capabilities

### New Capabilities

Tidak ada.

### Modified Capabilities

- `property-booking-models`: Menambahkan spesifikasi hak akses pengguna internal dan pembatasan isolasi data rekaman dokumen reservasi serta jadwal cicilan bagi pengguna portal.

## Impact

- **Files created:**
  - `addons/estate_booking/security/ir.model.access.csv`
  - `addons/estate_booking/security/security.xml`
- **Files modified:**
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 4 hours.
