## 1. Controller Routing & Availability Logic

- [x] 1.1 Tambahkan method `property_detail` pada `PropertyCatalogController` di `addons/estate_booking/controllers/main.py` dengan rute `/property/<int:property_id>`.
- [x] 1.2 Implementasikan validasi ketersediaan unit properti (`status == 'new'` dan `active == True`) dengan pengalihan aman kembali ke `/properties` jika unit tidak tersedia.

## 2. QWeb Property Detail View Template

- [x] 2.1 Buat berkas template QWeb `addons/estate_booking/views/portal_property_detail_templates.xml` yang mewarisi `website.layout` dilengkapi breadcrumb navigasi terstruktur.
- [x] 2.2 Rancang tata letak modern 2-kolom memuat galeri visual, deskripsi, tabel spesifikasi fisik komprehensif, ringkasan harga berstandar moneter multi-mata uang, serta tombol aksi pemesanan ("Book Now").

## 3. Manifest Registration and System Verification

- [x] 3.1 Daftarkan berkas `views/portal_property_detail_templates.xml` pada elemen `data` di `addons/estate_booking/__manifest__.py`.
- [x] 3.2 Lakukan pembaruan modul `estate_booking` pada lingkungan Odoo dan uji coba verifikasi respons HTTP serta alur navigasi properti.
