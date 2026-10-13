## ADDED Requirements

### Requirement: Formulir Checkout Reservasi Properti

The system MUST menyediakan antarmuka web formulir checkout `/booking/checkout` yang menampilkan ringkasan unit properti yang dipesan beserta kolom isian data identitas calon pembeli (nama lengkap, alamat email, dan nomor telepon) serta rincian biaya uang tanda jadi (*booking fee*).
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2.

#### Scenario: Pengunjung membuka formulir checkout untuk unit properti yang tersedia

- **WHEN** pengunjung mengakses URL formulir checkout dengan parameter `property_id` yang valid, aktif, dan berstatus `new`
- **THEN** sistem menyajikan halaman formulir checkout dengan ringkasan properti dan kolom isian data identitas pemesan dengan status HTTP 200

#### Scenario: Pengunjung membuka formulir checkout untuk properti yang tidak tersedia

- **WHEN** pengunjung mengakses formulir checkout untuk properti yang tidak valid, tidak aktif, atau tidak berstatus `new`
- **THEN** sistem mengalihkan pengunjung secara aman kembali ke halaman katalog properti `/properties`

### Requirement: Pemrosesan Data Checkout dan Pembuatan Draf Reservasi

The system MUST memproses data formulir checkout yang dikirimkan pengunjung, membuat atau mencocokkan kontak pelanggan (`res.partner`), dan menerbitkan dokumen draf reservasi baru (`estate.booking`) dengan status awal `draft` yang menyimpan nilai `booking_fee_paid` sesuai nilai uang tanda jadi unit terkait.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Pengguna mengirimkan data formulir checkout yang valid

- **WHEN** pengguna mengirimkan data identitas pemesan yang lengkap (nama, email, telepon) melalui formulir checkout
- **THEN** sistem mencatat atau memperbarui data kontak mitra (`res.partner`), membuat dokumen baru `estate.booking` dengan status `draft`, dan mengalihkan pengguna ke halaman konfirmasi pemesanan

#### Scenario: Pengguna mengirimkan formulir checkout dengan data tidak lengkap

- **WHEN** pengguna mengirimkan formulir checkout tanpa mengisi kolom wajib (nama atau email)
- **THEN** sistem mempertahankan formulir checkout dan menampilkan pesan galat validasi yang memandu pengguna melengkapi isian

### Requirement: Halaman Konfirmasi Reservasi Properti

The system MUST menyajikan halaman konfirmasi pemesanan `/booking/confirmation/<id>` yang menampilkan nomor referensi unik dokumen booking, rincian identitas pemesan, ringkasan unit properti, serta jumlah uang tanda jadi yang harus diselesaikan.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Pengguna mengakses halaman konfirmasi reservasi miliknya

- **WHEN** pengguna membuka URL konfirmasi untuk dokumen draf reservasi yang berhasil diterbitkan
- **THEN** sistem menyajikan rincian lengkap dokumen booking dengan status HTTP 200 dan tautan untuk melanjutkan ke pembayaran gerbang digital
