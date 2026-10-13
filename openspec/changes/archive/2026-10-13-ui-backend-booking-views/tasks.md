## 1. Booking Views Construction

- [x] 1.1 Membuat direktori `addons/estate_booking/views` jika belum ada.
- [x] 1.2 Membuat berkas `addons/estate_booking/views/estate_booking_views.xml` yang mendefinisikan Window Action (`estate_booking_action`) untuk model `estate.booking`.
- [x] 1.3 Menambahkan Search filter view pada `estate_booking_views.xml` dengan filter status (`draft`, `waiting_payment`, `confirmed`, `canceled`) dan group by properti serta klien.
- [x] 1.4 Menambahkan Tree (List) view pada `estate_booking_views.xml` yang menampilkan nomor referensi (`name`), properti (`property_id`), klien (`customer_id`), tanggal (`booking_date`), pembayaran awal (`booking_fee_paid`), dan status (`state`).
- [x] 1.5 Menambahkan Form view pada `estate_booking_views.xml` dengan header tombol alur transisi (`action_waiting_payment`, `action_confirm`, `action_cancel`), widget statusbar, sheet informasi reservasi, dan tab notebook berisi baris cicilan (`installment_ids`).

## 2. Installment Views Construction

- [x] 2.1 Membuat berkas `addons/estate_booking/views/estate_installment_views.xml` yang mendefinisikan Window Action (`estate_installment_action`) untuk model `estate.installment`.
- [x] 2.2 Menambahkan Search filter view pada `estate_installment_views.xml` dengan filter status (`unpaid`, `paid`, `late`) dan group by reservasi.
- [x] 2.3 Menambahkan Tree (List) view pada `estate_installment_views.xml` yang menampilkan reservasi (`booking_id`), keterangan (`name`), tanggal jatuh tempo (`due_date`), nilai tagihan (`amount`), dan status (`state`).
- [x] 2.4 Menambahkan Form view pada `estate_installment_views.xml` yang menyajikan detail reservasi, keterangan, tanggal jatuh tempo, nominal tagihan, faktur terkait, dan status pembayaran.

## 3. Navigation Menus and Manifest Integration

- [x] 3.1 Membuat berkas `addons/estate_booking/views/estate_booking_menus.xml` yang mendefinisikan menu kategori "Reservasi" di bawah root menu `estate.estate_property_root`, serta submenu untuk "Daftar Reservasi" dan "Jadwal Cicilan".
- [x] 3.2 Memperbarui `addons/estate_booking/__manifest__.py` untuk mendaftarkan file `views/estate_booking_views.xml`, `views/estate_installment_views.xml`, dan `views/estate_booking_menus.xml` pada urutan deklarasi `data` yang tepat.
- [x] 3.3 Memperbarui modul `estate_booking` pada container Odoo dan memverifikasi tidak ada error sintaks XML atau kesalahan dependensi ID saat memuat antarmuka backend.
