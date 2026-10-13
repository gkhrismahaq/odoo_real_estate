## 1. Controller Routing and Business Logic

- [x] 1.1 Tambahkan method `booking_checkout` pada controller di `addons/estate_booking/controllers/main.py` dengan rute GET `/booking/checkout` untuk menampilkan halaman formulir pemesanan unit properti baru.
- [x] 1.2 Implementasikan method `booking_checkout_submit` pada controller dengan rute POST `/booking/checkout/submit` untuk memvalidasi data form, mengelola data mitra (`res.partner`), dan menerbitkan dokumen draf `estate.booking`.
- [x] 1.3 Tambahkan method `booking_confirmation` pada controller dengan rute GET `/booking/confirmation/<int:booking_id>` untuk menampilkan rincian konfirmasi pemesanan sukses.

## 2. QWeb Checkout & Confirmation View Templates

- [x] 2.1 Buat berkas template QWeb `addons/estate_booking/views/portal_booking_checkout_templates.xml` yang memuat template `booking_checkout` dengan tata letak modern 2-kolom (formulir data pemesan dan ringkasan unit properti).
- [x] 2.2 Tambahkan template `booking_confirmation` pada berkas yang sama untuk menyajikan nomor referensi booking, rincian unit, dan jumlah uang tanda jadi yang harus diselesaikan.

## 3. Manifest Registration and System Verification

- [x] 3.1 Daftarkan berkas `views/portal_booking_checkout_templates.xml` pada elemen `data` di `addons/estate_booking/__manifest__.py`.
- [x] 3.2 Lakukan pembaruan modul `estate_booking` pada lingkungan Odoo dan uji coba end-to-end alur checkout mulai dari form input hingga penerbitan draf reservasi dan halaman konfirmasi.
