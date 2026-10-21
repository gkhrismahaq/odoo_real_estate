## 1. Domain Model Fields and Calculations

- [x] 1.1 Tambahkan field `installment_term` (Integer, default 12) dan computed field `remaining_amount` (Monetary) beserta method `_compute_remaining_amount()` pada model `estate.booking` (`addons/estate_booking/models/estate_booking.py`).
- [x] 1.2 Tambahkan validasi konstrain `@api.constrains('installment_term', 'booking_fee_paid')` pada `estate.booking` untuk menjamin jumlah termin selalu bernilai positif (> 0) dan uang tanda jadi tidak melebihi total harga properti.

## 2. Installment Schedule Generator and Lifecycle Integration

- [x] 2.1 Implementasikan method `action_generate_installments()` pada `estate.booking` yang mendistribusikan sisa kewajiban (`remaining_amount`) secara merata ke dalam sejumlah termin dengan penyesuaian pembulatan mata uang pada termin terakhir dan penetapan jatuh tempo bulanan bertahap (`relativedelta`).
- [x] 2.2 Tambahkan validasi proteksi integritas data pada `action_generate_installments()` untuk mencegah modifikasi atau regenerasi cicilan jika terdapat baris cicilan yang telah memiliki relasi faktur akuntansi (`invoice_id`).
- [x] 2.3 Perbarui method `action_confirm()` pada `estate.booking` agar secara otomatis memicu eksekusi `action_generate_installments()` saat dokumen reservasi beralih ke status `confirmed` dengan jaminan idempotensi.

## 3. Backend Views and User Interface Enhancements

- [x] 3.1 Perbarui tampilan form view `addons/estate_booking/views/estate_booking_views.xml` untuk menampilkan field konfigurasi `installment_term` dan sisa kewajiban `remaining_amount`.
- [x] 3.2 Tambahkan tombol aksi manual "Buat Jadwal Cicilan" pada header form view `estate_booking_views.xml` agar staf operasional dapat memperbarui draf cicilan sebelum penerbitan faktur.

## 4. Verification and End-to-End Testing

- [x] 4.1 Jalankan static analysis, validasi sintaks Python (AST check & import integrity), serta validasi XML schema (`xmllint`) untuk memastikan zero syntax/structural error.
- [x] 4.2 Uji coba alur end-to-end pembuatan cicilan: verifikasi bahwa ketika reservasi terkonfirmasi, baris `estate.installment` terbentuk secara otomatis, tanggal jatuh tempo tepat berjarak satu bulan, dan jumlah akumulasi angsuran sama persis dengan `remaining_amount`.
