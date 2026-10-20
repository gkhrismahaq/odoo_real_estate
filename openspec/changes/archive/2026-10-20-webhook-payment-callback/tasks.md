## 1. Model Webhook Notification Handling

- [x] 1.1 Override method `_process_notification_data(self, notification_data)` pada model `payment.transaction` di `addons/estate_booking/models/payment_transaction.py` untuk memproses callback status pembayaran dari provider secara native.
- [x] 1.2 Implementasikan logika verifikasi integritas nominal transaksi terhadap `booking_fee_paid` dan kesesuaian mata uang pada dokumen `estate.booking`.

## 2. Controller and Portal Status Presentation

- [x] 2.1 Perbarui method `booking_pay` pada controller di `addons/estate_booking/controllers/main.py` untuk mendeteksi status mutakhir transaksi (`done`, `pending`, `cancel`, `error`) dan menyediakan context render yang relevan.
- [x] 2.2 Perbarui template QWeb `addons/estate_booking/views/portal_booking_payment_templates.xml` dengan menambahkan kartu status umpan balik transaksi (sukses terverifikasi, menunggu verifikasi, atau gagal).

## 3. System Verification and Linting Scan

- [x] 3.1 Lakukan static code analysis dan validasi sintaks Python (AST compilation & import check) serta XML linting (`xmllint`) untuk memastikan zero technical issues.
- [x] 3.2 Uji coba alur callback notifikasi pembayaran (simulasi pemrosesan status sukses/done pada transaksi) dan pastikan integritas data transaksi terverifikasi dengan benar.
