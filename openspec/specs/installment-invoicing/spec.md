# installment-invoicing Specification

## Purpose

Menyediakan fungsionalitas otomatisasi pembuatan dan kalkulasi jadwal angsuran pembiayaan berkala (`estate.installment`) bagi dokumen reservasi properti (`estate.booking`) yang telah terkonfirmasi lunas uang tanda jadinya, membagi sisa nilai kewajiban pembayaran ke dalam termin bulanan secara terstruktur dan terintegrasi.

## Requirements

### Requirement: Pembentukan Otomatis Draf Jadwal Cicilan Pasca-Konfirmasi Reservasi

The system MUST secara otomatis membentuk deretan rekaman jadwal cicilan `estate.installment` ketika dokumen pemesanan `estate.booking` beralih ke status terkonfirmasi (`confirmed`), dengan jumlah baris yang sesuai dengan jumlah termin yang ditetapkan dan tanggal jatuh tempo bertahap setiap bulan.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Bagian 5.1 (`installment-invoicing`).
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 (Alur Proses Bisnis butir 4) & Bagian 3.2.

#### Scenario: Pembuatan baris cicilan secara reaktif saat reservasi dikonfirmasi

- **WHEN** dokumen pemesanan `estate.booking` berhasil beralih ke status `confirmed` (baik secara manual maupun otomatis dari notifikasi pembayaran)
- **THEN** sistem secara otomatis menginisiasi pembuatan deretan rekaman `estate.installment` berstatus `unpaid` dengan tanggal jatuh tempo bulanan bertahap mulai satu bulan sejak tanggal reservasi

#### Scenario: Idempotensi pembuatan jadwal cicilan pembiayaan

- **WHEN** proses konfirmasi dokumen reservasi `estate.booking` dieksekusi berulang kali pada reservasi yang telah memiliki jadwal cicilan
- **THEN** sistem tidak membuat duplikasi baris cicilan baru melainkan mempertahankan rekaman cicilan yang sudah ada

### Requirement: Perhitungan Nominal Angsuran dan Sisa Kewajiban Pembiayaan

The system MUST menghitung sisa kewajiban pembayaran properti (harga properti dikurangi nilai uang tanda jadi yang telah dibayarkan) dan mendistribusikannya secara merata ke dalam setiap termin cicilan dengan presisi mata uang yang konsisten.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2 (Model Data `estate.booking` dan `estate.installment`).

#### Scenario: Perhitungan nominal angsuran per termin secara presisi

- **WHEN** sistem menghitung jadwal cicilan untuk sisa kewajiban pembayaran tertentu dengan jumlah termin N
- **THEN** setiap baris cicilan menerima nominal sebesar sisa kewajiban dibagi N, dengan sisa pembulatan mata uang disesuaikan secara akurat pada baris termin terakhir agar total akumulasi cicilan sama persis dengan sisa kewajiban

#### Scenario: Validasi parameter jumlah termin cicilan

- **WHEN** pengguna memasukkan jumlah termin bernilai nol atau negatif pada dokumen reservasi
- **THEN** sistem menolak perhitungan dan menampilkan pesan validasi bahwa jumlah termin cicilan harus lebih besar dari 0

### Requirement: Pemicuan Pembuatan Jadwal Cicilan secara Manual

The system MUST menyediakan aksi manual bagi agen properti berwenang untuk meng-generate atau me-regenerasi draf jadwal cicilan pada dokumen reservasi yang telah terkonfirmasi selama belum ada baris cicilan yang diterbitkan fakturnya (`invoice_id`) atau berstatus lunas.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.4 (Hak Akses).

#### Scenario: Agen properti memperbarui jadwal cicilan secara manual

- **WHEN** agen properti menekan tombol pembuatan jadwal cicilan pada dokumen reservasi terkonfirmasi yang seluruh cicilannya masih berupa draf belum berfaktur
- **THEN** sistem meregenerasi baris jadwal cicilan baru sesuai parameter termin dan nominal terkini

#### Scenario: Pencegahan regenerasi cicilan yang sudah memiliki faktur akuntansi

- **WHEN** agen properti mencoba me-regenerasi jadwal cicilan pada dokumen reservasi yang memiliki cicilan yang telah terhubung dengan faktur akuntansi
- **THEN** sistem menolak tindakan tersebut dan menampilkan pesan kesalahan bahwa jadwal cicilan tidak dapat diubah karena telah terintegrasi dengan faktur

### Requirement: Penerbitan Draf Faktur Pelanggan dari Jadwal Cicilan

The system MUST menerbitkan dokumen faktur pelanggan (*Customer Invoice* / `account.move` dengan tipe `out_invoice`) berdasarkan data entitas `estate.installment`, menetapkan mitra pembeli (`customer_id`) dari dokumen reservasi terkait, mencantumkan nominal tagihan, mata uang, dan tanggal jatuh tempo, serta mencatat relasi `invoice_id` secara langsung.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Bagian 5.1 (`installment-invoicing`).
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.2 (Tujuan Bisnis), Bagian 3.1, & Bagian 3.2.

#### Scenario: Penerbitan faktur pelanggan secara manual oleh staf keuangan

- **WHEN** staf keuangan menekan tombol "Terbitkan Faktur" pada jadwal cicilan yang belum memiliki faktur
- **THEN** sistem membuat dokumen draf `account.move` (tipe `out_invoice`) baru dengan baris tagihan sesuai cicilan, mengaitkan ID faktur ke `estate.installment`, dan mengarahkan pengguna ke tampilan formulir faktur tersebut

#### Scenario: Pencegahan penerbitan faktur ganda untuk cicilan yang sama

- **WHEN** pengguna mencoba menerbitkan faktur untuk jadwal cicilan yang sudah memiliki relasi `invoice_id`
- **THEN** sistem menolak pembuatan faktur baru dan menampilkan pesan peringatan bahwa faktur untuk cicilan tersebut sudah pernah diterbitkan

### Requirement: Otomatisasi Penerbitan Draf Faktur Cicilan Jatuh Tempo

The system MUST secara berkala melalui scheduled action (cron job harian) memindai dan menerbitkan dokumen draf faktur pelanggan secara otomatis untuk seluruh jadwal cicilan `estate.installment` yang telah mencapai atau melewati batas tanggal jatuh tempo (`due_date <= context_today`) dan belum memiliki faktur akuntansi.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Bagian 5.1 (`installment-invoicing`).
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 (Alur Proses Bisnis butir 4) & Bagian 3.2.

#### Scenario: Eksekusi otomatis cron job untuk cicilan jatuh tempo

- **WHEN** scheduled action harian dijalankan dan mendeteksi terdapat baris cicilan berstatus `unpaid` dengan tanggal jatuh tempo hari ini atau sebelumnya serta belum memiliki `invoice_id`
- **THEN** sistem secara otomatis menerbitkan draf `account.move` untuk setiap cicilan tersebut dan mencatat referensi `invoice_id` tanpa intervensi manual

#### Scenario: Pengabaian cicilan yang belum jatuh tempo atau telah berfaktur

- **WHEN** scheduled action harian memindai data cicilan
- **THEN** sistem mengabaikan baris cicilan yang tanggal jatuh temponya masih di masa mendatang atau baris cicilan yang telah memiliki relasi faktur sebelumnya

### Requirement: Sinkronisasi Status Pembayaran Cicilan dengan Faktur Akuntansi

The system MUST menyinkronkan status pelunasan pada entitas cicilan `estate.installment` (`state`) berdasarkan status pembayaran faktur terkait (`payment_state` pada dokumen `account.move`), mengalihkan status cicilan menjadi `paid` saat faktur dinyatakan lunas, dan menandai `late` jika tanggal jatuh tempo terlewati tanpa pelunasan faktur.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2 (Model Data `estate.installment`).

#### Scenario: Status cicilan otomatis menjadi lunas saat faktur terbayar penuh

- **WHEN** faktur akuntansi yang terhubung dengan cicilan diverifikasi lunas (`payment_state` bernilai `paid` atau `in_payment`)
- **THEN** sistem memperbarui status `state` pada rekaman `estate.installment` terkait menjadi `paid`

#### Scenario: Status cicilan ditandai terlambat saat jatuh tempo terlewati

- **WHEN** jadwal cicilan belum lunas dan tanggal jatuh tempo telah terlewati
- **THEN** sistem menyajikan atau memperbarui status cicilan menjadi `late` (Terlambat)

