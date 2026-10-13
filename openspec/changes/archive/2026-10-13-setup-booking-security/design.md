## Context

Lihat alasan perubahan pada `proposal.md`. Model `estate.booking` dan `estate.installment` telah diimplementasikan, namun belum dilengkapi dengan Access Control List (ACL) dan Record Rules. Odoo 17 memerlukan definisi akses di `ir.model.access.csv` agar model dapat diakses oleh grup pengguna yang tepat tanpa memunculkan warning keamanan. TSD Bagian 3.4 secara spesifik menetapkan pembagian peran di mana Agen Properti memiliki hak CRUD penuh, Klien Portal hanya berhak membaca data miliknya sendiri, dan Pengunjung Publik tidak memiliki akses ke rekaman reservasi.

## Goals / Non-Goals

**Goals:**

- Membuat file `addons/estate_booking/security/ir.model.access.csv` yang menetapkan hak akses model `estate.booking` dan `estate.installment` bagi grup internal (`base.group_user`) dengan izin penuh (`1,1,1,1`) dan grup portal (`base.group_portal`) dengan izin baca (`1,0,0,0`).
- Membuat file `addons/estate_booking/security/security.xml` yang mendefinisikan aturan rekaman (`ir.rule`) agar Klien Portal hanya dapat membaca reservasi dan cicilan miliknya sendiri (`customer_id = user.partner_id.id` / `booking_id.customer_id = user.partner_id.id`).
- Mendaftarkan file keamanan ke dalam daftar `data` pada `addons/estate_booking/__manifest__.py`.
- Menghilangkan warning ketiadaan aturan akses pada saat modul dimuat.

**Non-Goals:**

- Membuat tampilan UI (Form/Tree) atau menu backend (dialokasikan ke change `ui-backend-booking-views`).
- Membuat antarmuka portal website atau controller portal (dialokasikan ke Fase 3).
- Mengubah arsitektur atau definisi field pada model Python yang telah ada.

## Decisions

### 1. Definisi Access Control List (ACL) pada `ir.model.access.csv`

- **Rationale:** Model `estate.booking` dan `estate.installment` membutuhkan entri ACL eksplisit. Grup Agen Properti (`base.group_user`) diberikan hak penuh (`perm_read=1, perm_write=1, perm_create=1, perm_unlink=1`) untuk mengelola seluruh data operasional reservasi dan jadwal cicilan. Grup Klien Portal (`base.group_portal`) diberikan hak membaca dasar (`perm_read=1, perm_write=0, perm_create=0, perm_unlink=0`), sedangkan hak untuk public sengaja tidak diberikan (akses ditolak secara default).
- **Alternatives Considered:** Memberikan hak akses tanpa menspesifikasikan grup (`group_id` kosong); ditolak karena akan membuka akses ke seluruh user secara global tanpa membedakan peran Agen dan Klien.

### 2. Isolasi Data Multi-Tenant Menggunakan Record Rules (`security.xml`)

- **Rationale:** ACL hanya mengatur izin level model, sehingga diperlukan Record Rule (`ir.rule`) pada `security.xml` untuk membatasi rekaman data yang boleh dibaca oleh pengguna portal.
  - Untuk `estate.booking`: Domain filter `[('customer_id', '=', user.partner_id.id)]` diterapkan khusus pada grup `base.group_portal`.
  - Untuk `estate.installment`: Domain filter `[('booking_id.customer_id', '=', user.partner_id.id)]` diterapkan khusus pada grup `base.group_portal`.
  Dengan mekanisme ini, keamanan dan privasi data pelanggan terjaga secara mutlak di tingkat query ORM database Odoo.
- **Alternatives Considered:** Melakukan filter record hanya di level web controller/QWeb; ditolak karena rentan celah keamanan dan inkonsistensi jika data diakses via JSON-RPC atau API lain.

### 3. Pendaftaran File Keamanan pada Manifest

- **Rationale:** File `security/security.xml` dan `security/ir.model.access.csv` didaftarkan ke dalam key `data` pada `__manifest__.py`. Urutan ini memuat record rules dan ACL secara otomatis setiap kali modul diinstal atau di-upgrade.
- **Alternatives Considered:** Menggabungkan record rules ke dalam manifest modul lain; ditolak karena aturan keamanan reservasi merupakan bagian inheren dari modul `estate_booking`.

## Risks / Trade-offs

- Pengguna Administrator/Superuser mem-bypass Record Rule secara bawaan di Odoo → Ini adalah perilaku standar Odoo; verifikasi record rule harus dilakukan dengan pengguna non-admin (portal user) untuk memastikan domain berjalan efektif.

## Migration Plan

1. Buat direktori `addons/estate_booking/security/`.
2. Tulis `ir.model.access.csv` dan `security.xml`.
3. Perbarui `__manifest__.py` dengan mendaftarkan kedua file tersebut.
4. Jalankan update modul `estate_booking` pada database Odoo dan verifikasi bahwa tidak ada warning keamanan yang tersisa.
