## Why

Meskipun sistem telah berhasil menerbitkan faktur pelanggan (`account.move`) dari jadwal cicilan (`estate.installment`), klien pembeli properti belum memiliki akses antarmuka mandiri (*self-service portal*) untuk memantau ringkasan pemesanan, jadwal jatuh tempo termin cicilan, dan status pelunasan faktur secara langsung. Ketiadaan akses portal ini memaksa klien melakukan konfirmasi berulang secara manual kepada agen properti, yang menghambat efisiensi operasional dan transparansi finansial. Mengekspos jadwal pembiayaan dan faktur tagihan ke dalam antarmuka Portal Pelanggan Odoo bawaan (`/my` dan `/my/invoices`) sangat esensial untuk memberikan visibilitas penuh bagi klien dan memfasilitasi penyelesaian pembayaran cicilan lanjutan secara mandiri.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Capability `installment-invoicing`, Change `ui-customer-portal-invoices`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.2 (Tujuan Bisnis), Bagian 2.1 (Profil Pengguna Klien), Bagian 2.2 (Alur Proses Bisnis butir 5), & Bagian 3.4 (Hak Akses Portal).

## What Changes

- Mengembangkan controller portal `CustomerPortal` pada `addons/estate_booking/controllers/portal.py` untuk mengintegrasikan menu "Reservasi Properti" pada beranda portal pelanggan (`/my` dan `/my/home`), lengkap dengan counter dokumen pemesanan aktif milik mitra login.
- Menyediakan rute web portal `/my/bookings` untuk menampilkan daftar riwayat pemesanan properti milik klien beserta status reservasi dan jumlah tagihan.
- Menyediakan rute web portal `/my/bookings/<int:booking_id>` untuk menampilkan detail dokumen reservasi, informasi unit properti, uang tanda jadi, dan tabel lengkap jadwal cicilan (`estate.installment`) disertai status pelunasan dan tautan langsung ke faktur pelanggan (`/my/invoices/<invoice_id>`).
- Membuat template QWeb portal `addons/estate_booking/views/portal_estate_booking_templates.xml` dengan desain responsif berbasis Bootstrap standar Odoo 17 untuk halaman daftar reservasi, halaman detail reservasi, serta widget kartu menu beranda portal.
- Mendaftarkan controller baru pada `addons/estate_booking/controllers/__init__.py` dan mendaftarkan file template XML pada `addons/estate_booking/__manifest__.py`.

## Capabilities

### New Capabilities

Tidak ada.

### Modified Capabilities

- `installment-invoicing`: Menambahkan kemampuan eksposur jadwal cicilan dan faktur pelanggan pada antarmuka web portal klien Odoo (`/my/bookings`, `/my/invoices`), transparansi status penagihan termin mandiri bagi pembeli, serta navigasi pembayaran faktur online langsung dari portal.

## Impact

- **Files created:**
  - `addons/estate_booking/controllers/portal.py`
  - `addons/estate_booking/views/portal_estate_booking_templates.xml`
  - `openspec/changes/ui-customer-portal-invoices/specs/installment-invoicing/spec.md`
- **Files modified:**
  - `addons/estate_booking/__manifest__.py`
  - `addons/estate_booking/controllers/__init__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 3 hours.
