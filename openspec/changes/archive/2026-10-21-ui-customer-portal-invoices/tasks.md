## 1. Portal Controller Implementation

- [x] 1.1 Kembangkan controller portal `EstateBookingPortal` yang mewarisi `CustomerPortal` pada `addons/estate_booking/controllers/portal.py` serta override method `_prepare_home_portal_values()` untuk menyuntikkan counter reservasi (`booking_count`).
- [x] 1.2 Implementasikan rute web portal `/my/bookings` untuk menampilkan daftar riwayat dokumen reservasi milik klien login dengan proteksi domain mitra dan pengurutan terindeks.
- [x] 1.3 Implementasikan rute web portal detail `/my/bookings/<int:booking_id>` dengan validasi kepemilikan dokumen (anti-IDOR) serta penyajian data pemesanan dan jadwal termin cicilan.
- [x] 1.4 Daftarkan controller portal baru ke dalam file inisialisasi controller `addons/estate_booking/controllers/__init__.py`.

## 2. Portal QWeb Templates Development

- [x] 2.1 Buat template portal card `portal_my_home_estate_booking` pada `addons/estate_booking/views/portal_estate_booking_templates.xml` yang meng-inherit `portal.portal_my_home` untuk menampilkan tautan dan counter "Reservasi Properti".
- [x] 2.2 Buat template breadcrumbs dan list view portal `portal_my_bookings` pada `portal_estate_booking_templates.xml` dengan layout responsif Bootstrap 5 dan tabel ringkasan pemesanan.
- [x] 2.3 Buat template detail view portal `portal_my_booking_detail` pada `portal_estate_booking_templates.xml` yang menyajikan rincian unit properti, status pembayaran uang muka, tabel jadwal termin cicilan (`estate.installment`), dan tautan langsung ke faktur Odoo (`/my/invoices/<invoice_id>`).
- [x] 2.4 Daftarkan modul dependensi `portal` dan file template `views/portal_estate_booking_templates.xml` ke dalam manifest modul `addons/estate_booking/__manifest__.py`.

## 3. Verification and End-to-End Testing

- [x] 3.1 Jalankan static analysis, validasi sintaks Python (AST check & import integrity), serta validasi XML schema (`xmllint`) pada seluruh file modul yang dibuat atau dimodifikasi.
- [x] 3.2 Uji coba alur portal: verifikasi render counter beranda `/my/home`, akses daftar `/my/bookings`, proteksi akses data antar klien (anti-IDOR) pada `/my/bookings/<id>`, serta navigasi tautan faktur aktif.
