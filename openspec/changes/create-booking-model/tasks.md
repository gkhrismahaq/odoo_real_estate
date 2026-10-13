## 1. Booking Model Foundation

- [x] 1.1 Membuat dan mendaftarkan model `estate.booking` pada paket `addons/estate_booking/models`.
- [x] 1.2 Menambahkan field referensi, relasi properti, relasi klien, dan tanggal transaksi sesuai TSD Bagian 3.2.
- [x] 1.3 Menambahkan `booking_fee_paid` bertipe Monetary beserta field mata uang teknis dengan nilai awal mata uang perusahaan aktif.
- [x] 1.4 Menambahkan relasi ke `payment.transaction` tanpa membuat atau memproses transaksi pembayaran.

## 2. Booking Relationships and State

- [x] 2.1 Menambahkan relasi balik `booking_ids` pada perluasan `estate.property` menggunakan inverse `property_id`.
- [x] 2.2 Menambahkan relasi `installment_ids` dari reservasi ke `estate.installment` sesuai TSD, tanpa mengimplementasikan model atau pembuatan jadwal cicilan.
- [x] 2.3 Menambahkan field `state` dengan nilai `draft`, `waiting_payment`, `confirmed`, dan `canceled`, serta nilai awal `draft`.
- [x] 2.4 Mengimplementasikan tindakan transisi berurutan draft ke menunggu pembayaran, menunggu pembayaran ke terkonfirmasi, dan terkonfirmasi ke dibatalkan tanpa mengubah status properti.

## 3. Verification

- [x] 3.1 Memeriksa bahwa semua model baru dan perluasan model terimpor dari file `__init__.py` yang tepat.
- [x] 3.2 Memverifikasi deklarasi field, nama model relasi, pilihan state, dan arah relasi terhadap TSD Bagian 3.2–3.3 serta delta spec.
- [x] 3.3 Menjalankan pemeriksaan registry atau pembaruan modul Odoo yang tersedia untuk memastikan relasi model dapat dimuat, lalu mencatat hasilnya.
