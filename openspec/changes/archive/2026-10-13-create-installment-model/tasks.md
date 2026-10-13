## 1. Installment Model Foundation

- [x] 1.1 Membuat model `estate.installment` pada file `addons/estate_booking/models/estate_installment.py`.
- [x] 1.2 Mendaftarkan modul model baru pada `addons/estate_booking/models/__init__.py`.
- [x] 1.3 Menambahkan field relasi inverse `booking_id` ke `estate.booking` dengan perilaku `ondelete='cascade'` sesuai TSD Bagian 3.2.
- [x] 1.4 Menambahkan field keterangan `name` dan tanggal jatuh tempo `due_date` bertipe Date.

## 2. Installment Accounting and State

- [x] 2.1 Menambahkan field `amount` bertipe Monetary beserta field mata uang teknis `currency_id` yang tersinkronisasi dengan reservasi.
- [x] 2.2 Menambahkan field relasi faktur `invoice_id` ke model `account.move` tanpa memicu pembuatan faktur otomatis.
- [x] 2.3 Menambahkan field status `state` dengan pilihan `unpaid`, `paid`, dan `late` serta nilai default `unpaid`.

## 3. Verification and Registry Validation

- [x] 3.1 Memeriksa kepatuhan sintaks Python dan memastikan seluruh model terimpor dengan benar di level paket.
- [x] 3.2 Menjalankan pembaruan modul `estate_booking` pada database Odoo untuk memvalidasi integrasi relasi model `estate.installment` dan `estate.booking`.
- [x] 3.3 Memverifikasi kestabilan registry Odoo dan memastikan endpoint HTTP tidak lagi mengalami 500 Internal Server Error.
