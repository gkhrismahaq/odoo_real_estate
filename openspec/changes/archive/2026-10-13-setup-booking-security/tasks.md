## 1. Access Control List Setup

- [x] 1.1 Membuat direktori `addons/estate_booking/security`.
- [x] 1.2 Menambahkan file `addons/estate_booking/security/ir.model.access.csv` dengan hak akses penuh (`1,1,1,1`) untuk grup internal `base.group_user` pada model `estate.booking` dan `estate.installment`.
- [x] 1.3 Menambahkan entri hak baca (`1,0,0,0`) pada `ir.model.access.csv` untuk grup portal `base.group_portal` pada model `estate.booking` dan `estate.installment`.

## 2. Record Rules Definition

- [x] 2.1 Membuat file `addons/estate_booking/security/security.xml` dengan struktur XML standar Odoo.
- [x] 2.2 Menambahkan record rule `ir.rule` pada `security.xml` untuk model `estate.booking` yang membatasi pembacaan data hanya milik pengguna portal (`customer_id = user.partner_id.id`).
- [x] 2.3 Menambahkan record rule `ir.rule` pada `security.xml` untuk model `estate.installment` yang membatasi pembacaan data hanya milik pengguna portal (`booking_id.customer_id = user.partner_id.id`).

## 3. Manifest Integration and Validation

- [x] 3.1 Mendaftarkan file `security/security.xml` dan `security/ir.model.access.csv` pada key `data` di `addons/estate_booking/__manifest__.py`.
- [x] 3.2 Menjalankan pembaruan modul `estate_booking` pada database Odoo dan memverifikasi tidak ada warning atau error hak akses saat registrasi model dimuat.
- [x] 3.3 Menguji evaluasi domain record rule melalui environment shell Odoo untuk memastikan filter partner akun portal berfungsi sesuai spesifikasi.
