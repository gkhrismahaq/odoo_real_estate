## ADDED Requirements

### Requirement: Penangkapan Notifikasi Gateway Pembayaran (Webhook Callback)

The system MUST menangkap data notifikasi dan sinyal umpan balik (*webhook/callback*) dari penyedia pembayaran digital melalui metode pemrosesan notifikasi transaksi (`_process_notification_data`) pada rekaman transaksi yang terhubung dengan dokumen reservasi `estate.booking`.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.3.
> **Reference:** [Roadmap](../../../../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

#### Scenario: Pemrosesan sinyal notifikasi pembayaran berhasil dari provider

- **WHEN** penyedia pembayaran mengirimkan notifikasi data callback transaksi berstatus sukses (`done`) untuk dokumen reservasi
- **THEN** sistem memproses data notifikasi, memvalidasi keberhasilan transaksi pembayaran, dan memperbarui status rekaman `payment.transaction` menjadi `done`

#### Scenario: Pemrosesan sinyal notifikasi pembayaran tertunda atau gagal

- **WHEN** penyedia pembayaran mengirimkan notifikasi callback transaksi berstatus tertunda (`pending`), dibatalkan (`cancel`), atau gagal (`error`)
- **THEN** sistem mencatat status terkini pada rekaman transaksi tanpa menandai pembayaran sebagai berhasil diselesaikan

### Requirement: Validasi Integritas Data Pembayaran Tanda Jadi

The system MUST memverifikasi integritas data transaksi pembayaran saat memproses notifikasi, memastikan bahwa nilai nominal yang dibayarkan cocok dengan nilai tagihan uang tanda jadi (`booking_fee_paid`) dan mata uang pada dokumen reservasi `estate.booking`.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.2 & 3.3.

#### Scenario: Integritas nominal dan mata uang pembayaran valid

- **WHEN** data notifikasi pembayaran diverifikasi dan nominal pembayaran sama dengan nilai `booking_fee_paid` serta mata uang transaksi sesuai
- **THEN** sistem menetapkan status transaksi sebagai pembayaran yang terverifikasi sah dan siap untuk pembaruan status pemesanan

#### Scenario: Ketidakcocokan nominal pembayaran terdeteksi

- **WHEN** data notifikasi pembayaran menunjukkan nominal yang lebih kecil dari nilai `booking_fee_paid`
- **THEN** sistem menandai transaksi sebagai anomali pembayaran (*mismatch error*) dan mencegah transaksi dinyatakan sebagai pembayaran penuh yang sah
