## 1. Data Model Extension and Payment Logic

- [x] 1.1 Buat model ekstensi `payment.transaction` pada `addons/estate_booking/models/payment_transaction.py` dengan menambahkan field relasi `booking_id = fields.Many2one("estate.booking")` guna mendukung relasi dua arah standar Odoo.
- [x] 1.2 Daftarkan modul model baru `payment_transaction` pada `addons/estate_booking/models/__init__.py`.
- [x] 1.3 Tambahkan business method `_create_or_get_payment_transaction(provider_id=None)` pada model `estate.booking` (`addons/estate_booking/models/estate_booking.py`) untuk menginisiasi rekaman transaksi `payment.transaction`, mengaitkan relasinya, dan mengeksekusi transisi status reservasi ke `waiting_payment`.

## 2. Controller Routing and Flow Integration

- [x] 2.1 Tambahkan method `booking_pay` pada controller di `addons/estate_booking/controllers/main.py` dengan rute GET `/booking/pay/<int:booking_id>` untuk validasi dokumen booking, inisiasi transaksi pembayaran tanda jadi via model, dan penyiapan data payment provider Odoo.
- [x] 2.2 Perbarui method `booking_confirmation` pada controller untuk memastikan ketersediaan data transaksi serta konteks kelanjutan pembayaran yang konsisten.

## 3. QWeb Portal Templates and UI Enhancement

- [x] 3.1 Buat berkas template QWeb `addons/estate_booking/views/portal_booking_payment_templates.xml` yang memuat template `booking_payment` untuk menampilkan ringkasan tagihan uang tanda jadi dan integrasi antarmuka pemrosesan pembayaran Odoo.
- [x] 3.2 Perbarui template `booking_confirmation` pada `addons/estate_booking/views/portal_booking_checkout_templates.xml` dengan menyematkan tombol aksi utama "Lanjutkan ke Pembayaran" menuju rute `/booking/pay/<booking_id>`.

## 4. Manifest Registration and System Verification

- [x] 4.1 Daftarkan berkas view baru `views/portal_booking_payment_templates.xml` pada daftar `data` di `addons/estate_booking/__manifest__.py`.
- [x] 4.2 Lakukan pembaruan modul `estate_booking` pada lingkungan Odoo dan uji coba end-to-end alur inisiasi pembayaran mulai dari konfirmasi reservasi, pembuatan referensi `payment.transaction`, hingga penyajian antarmuka pembayaran provider Odoo.
