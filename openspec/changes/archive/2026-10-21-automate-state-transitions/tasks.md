## 1. Domain Model State Transition Enhancements

- [x] 1.1 Perbarui method `action_confirm()` pada `estate.booking` (`addons/estate_booking/models/estate_booking.py`) untuk mengalihkan status unit properti terkait (`property_id.status = 'reserved'`) secara otomatis dan menjamin idempotensi status.
- [x] 1.2 Perbarui method `action_cancel()` pada `estate.booking` untuk mengembalikan status unit properti menjadi `new` apabila tidak terdapat pemesanan terkonfirmasi aktif lainnya pada unit tersebut.

## 2. Payment Transaction Webhook Trigger

- [x] 2.1 Perbarui method `_process_notification_data()` pada `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`) untuk memicu eksekusi `booking_id.action_confirm()` secara otomatis saat transaksi berstatus `done`.
- [x] 2.2 Perbarui method controller `booking_pay_simulate` pada `addons/estate_booking/controllers/main.py` agar memicu alur konfirmasi otomatis status pemesanan dan unit secara konsisten.

## 3. Portal UI and Confirmation View Updates

- [x] 3.1 Perbarui template konfirmasi pemesanan `addons/estate_booking/views/portal_booking_checkout_templates.xml` untuk menampilkan badge status Terkonfirmasi dan informasi unit terkunci pasca-pembayaran.
- [x] 3.2 Perbarui template portal pembayaran `addons/estate_booking/views/portal_booking_payment_templates.xml` untuk menyajikan tautan konfirmasi serta instruksi tahap selanjutnya ketika reservasi telah terkonfirmasi.

## 4. Verification and End-to-End Testing

- [x] 4.1 Lakukan static code analysis, validasi sintaks Python (AST compilation & import check), serta XML linting (`xmllint`) untuk memastikan zero technical debt.
- [x] 4.2 Uji coba alur transisi status end-to-end: verifikasi bahwa ketika transaksi pembayaran berstatus `done`, status `estate.booking` otomatis menjadi `confirmed` dan status `estate.property` otomatis terkunci menjadi `reserved`.
