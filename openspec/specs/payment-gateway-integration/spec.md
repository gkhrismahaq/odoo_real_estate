# payment-gateway-integration Specification

## Purpose

Menghubungkan proses pemesanan unit properti (`estate.booking`) dengan mesin transaksi pembayaran standar Odoo (`payment.transaction`) untuk menginisiasi pembayaran uang tanda jadi (*booking fee*) melalui Payment Provider Odoo dan mengalihkan status pemesanan ke tahap menunggu pembayaran.

## Requirements

### Requirement: Inisiasi Transaksi Pembayaran Uang Tanda Jadi

The system MUST membuat atau mengaitkan rekaman transaksi pembayaran `payment.transaction` untuk dokumen `estate.booking` dengan nilai nominal sebesar uang tanda jadi (`booking_fee_paid`), mata uang yang valid, serta mengaitkan relasi dokumen pemesanan secara dua arah dengan referensi transaksi unik.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.3, 2.2, & 3.2.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

#### Scenario: Inisiasi transaksi pembayaran untuk reservasi berstatus draft

- **WHEN** pengguna atau sistem menginisiasi proses pembayaran untuk dokumen reservasi yang masih berstatus `draft`
- **THEN** sistem membuat rekaman baru `payment.transaction` dengan nilai nominal sesuai `booking_fee_paid`, mata uang reservasi, mitra pembeli terkait, dan menyimpan referensi relasi transaksi pada dokumen `estate.booking`

#### Scenario: Menggunakan kembali transaksi pembayaran tertunda yang sudah ada

- **WHEN** pengguna membuka kembali proses pembayaran untuk dokumen reservasi yang telah memiliki transaksi pembayaran berstatus belum selesai (*draft* atau *pending*)
- **THEN** sistem tidak membuat transaksi baru yang berlebihan (mencegah duplikasi) melainkan menggunakan kembali rekaman `payment.transaction` yang relevan

### Requirement: Transisi Status Reservasi ke Menunggu Pembayaran

The system MUST mengubah status dokumen reservasi `estate.booking` dari `draft` menjadi `waiting_payment` ketika proses transaksi pembayaran diinisiasi oleh pengguna.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.3.

#### Scenario: Perubahan status otomatis saat alur pembayaran dimulai

- **WHEN** transaksi pembayaran tanda jadi berhasil diinisiasi untuk reservasi yang berstatus `draft`
- **THEN** status dokumen reservasi `estate.booking` secara otomatis beralih menjadi `waiting_payment`

#### Scenario: Pencegahan inisiasi pembayaran untuk reservasi yang tidak valid

- **WHEN** pengguna mencoba menginisiasi pembayaran untuk dokumen reservasi yang telah berstatus `confirmed` atau `canceled`
- **THEN** sistem menolak pembuatan transaksi baru dan mengembalikan pesan bahwa pembayaran untuk reservasi tersebut tidak dapat diproses

### Requirement: Penyajian Antarmuka Pembayaran Provider Digital

The system MUST menyediakan antarmuka web pembayaran pada rute `/booking/pay/<int:booking_id>` yang memvalidasi ketersediaan unit dan status reservasi, menampilkan ringkasan rincian tagihan uang tanda jadi, serta menyajikan formulir pemrosesan pembayaran bawaan Odoo (*payment processing form*) yang terhubung dengan penyedia pembayaran aktif (misalnya *Test Provider*).
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.3 & 2.2.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

#### Scenario: Pengguna mengakses rute pembayaran booking yang valid

- **WHEN** pengguna mengakses URL `/booking/pay/<id>` dengan ID booking yang valid dan berstatus `draft` atau `waiting_payment`
- **THEN** sistem menyajikan halaman pembayaran dengan status HTTP 200 lengkap dengan ringkasan unit, jumlah tagihan tanda jadi, dan formulir integrasi penyedia pembayaran Odoo

#### Scenario: Pengguna mengakses rute pembayaran untuk booking yang tidak valid

- **WHEN** pengguna mengakses URL `/booking/pay/<id>` untuk ID booking yang tidak ditemukan di dalam sistem
- **THEN** sistem mengalihkan pengguna kembali ke halaman katalog properti `/properties` secara aman

### Requirement: Tautan Aksi Pembayaran pada Halaman Konfirmasi Reservasi

The system MUST menyediakan tombol aksi interaktif "Lanjutkan ke Pembayaran" pada antarmuka web konfirmasi pemesanan `/booking/confirmation/<int:booking_id>` yang mengarahkan pengguna secara langsung ke halaman rute pemrosesan transaksi pembayaran `/booking/pay/<id>`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2.

#### Scenario: Menampilkan tombol lanjutkan ke pembayaran pada halaman konfirmasi

- **WHEN** halaman konfirmasi reservasi dimuat untuk dokumen booking yang belum selesai dibayar
- **THEN** antarmuka menampilkan tombol aksi utama "Lanjutkan ke Pembayaran" yang memiliki target tautan menuju `/booking/pay/<booking_id>`

### Requirement: Penangkapan Notifikasi Gateway Pembayaran (Webhook Callback)

The system MUST menangkap data notifikasi dan sinyal umpan balik (*webhook/callback*) dari penyedia pembayaran digital melalui metode pemrosesan notifikasi transaksi (`_process_notification_data`) pada rekaman transaksi yang terhubung dengan dokumen reservasi `estate.booking`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.3.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

#### Scenario: Pemrosesan sinyal notifikasi pembayaran berhasil dari provider

- **WHEN** penyedia pembayaran mengirimkan notifikasi data callback transaksi berstatus sukses (`done`) untuk dokumen reservasi
- **THEN** sistem memproses data notifikasi, memvalidasi keberhasilan transaksi pembayaran, dan memperbarui status rekaman `payment.transaction` menjadi `done`

#### Scenario: Pemrosesan sinyal notifikasi pembayaran tertunda atau gagal

- **WHEN** penyedia pembayaran mengirimkan notifikasi callback transaksi berstatus tertunda (`pending`), dibatalkan (`cancel`), atau gagal (`error`)
- **THEN** sistem mencatat status terkini pada rekaman transaksi tanpa menandai pembayaran sebagai berhasil diselesaikan

### Requirement: Validasi Integritas Data Pembayaran Tanda Jadi

The system MUST memverifikasi integritas data transaksi pembayaran saat memproses notifikasi, memastikan bahwa nilai nominal yang dibayarkan cocok dengan nilai tagihan uang tanda jadi (`booking_fee_paid`) dan mata uang pada dokumen reservasi `estate.booking`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2 & 3.3.

#### Scenario: Integritas nominal dan mata uang pembayaran valid

- **WHEN** data notifikasi pembayaran diverifikasi dan nominal pembayaran sama dengan nilai `booking_fee_paid` serta mata uang transaksi sesuai
- **THEN** sistem menetapkan status transaksi sebagai pembayaran yang terverifikasi sah dan siap untuk pembaruan status pemesanan

#### Scenario: Ketidakcocokan nominal pembayaran terdeteksi

- **WHEN** data notifikasi pembayaran menunjukkan nominal yang lebih kecil dari nilai `booking_fee_paid`
- **THEN** sistem menandai transaksi sebagai anomali pembayaran (*mismatch error*) dan mencegah transaksi dinyatakan sebagai pembayaran penuh yang sah
