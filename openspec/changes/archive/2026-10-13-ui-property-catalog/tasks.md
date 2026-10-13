## 1. Controller Scaffolding and Routing

- [x] 1.1 Membuat direktori `addons/estate_booking/controllers` dan file `addons/estate_booking/controllers/__init__.py`.
- [x] 1.2 Mengimpor modul `controllers` ke dalam `addons/estate_booking/__init__.py`.
- [x] 1.3 Membuat file `addons/estate_booking/controllers/main.py` yang mendefinisikan kelas controller dengan route publik `/properties` (`auth='public'`, `website=True`).
- [x] 1.4 Mengimplementasikan pengambilan data properti berstatus `new` dan aktif secara aman via `sudo()` pada controller serta merendernya ke template QWeb `estate_booking.property_catalog`.

## 2. QWeb Catalog Template Construction

- [x] 2.1 Membuat berkas `addons/estate_booking/views/portal_property_catalog_templates.xml` dengan struktur template QWeb yang mewarisi `website.layout`.
- [x] 2.2 Merancang header halaman katalog dan tata letak grid kartu properti responsif berbasis Bootstrap 5.
- [x] 2.3 Mengimplementasikan komponen kartu properti yang menampilkan nama, tipe, harga bukaan, kode pos, kamar tidur, luas bangunan, dan tombol detail.
- [x] 2.4 Menambahkan blok penanganan tampilan ramah ketika katalog kosong (*empty state*).

## 3. Manifest Integration and Testing

- [x] 3.1 Mendaftarkan file `views/portal_property_catalog_templates.xml` pada key `data` di `addons/estate_booking/__manifest__.py`.
- [x] 3.2 Memperbarui modul `estate_booking` pada container Odoo dan memverifikasi tidak ada error parsing template QWeb atau registrasi controller.
- [x] 3.3 Menguji akses HTTP ke endpoint publik `/properties` dan memastikan respons mengembalikan status 200 OK dengan konten katalog yang sesuai.
