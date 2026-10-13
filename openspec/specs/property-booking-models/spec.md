# property-booking-models Specification

## Purpose

Menambahkan kemampuan bagi model properti yang sudah ada untuk menyimpan informasi nilai tanda jadi (booking fee), daftar reservasi terkait, dan memiliki status khusus saat dipesan oleh klien.

## Requirements

### Requirement: Atribut Pemesanan Properti

The system MUST menyimpan informasi nilai uang tanda jadi (booking fee) yang dibutuhkan untuk memesan sebuah properti, beserta referensi daftar reservasi yang terkait.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Menentukan nilai pemesanan

- **WHEN** agen properti membuat atau memperbarui properti
- **THEN** sistem memungkinkan agen untuk menginput nilai uang (Monetary) ke dalam kolom `booking_fee`

### Requirement: Status Dipesan pada Properti

The system MUST mendukung perubahan status properti menjadi "dipesan" (reserved) ketika proses reservasi telah dikonfirmasi, untuk mencegah pemesanan ganda.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Reservasi sukses

- **WHEN** sebuah dokumen reservasi terhadap properti berhasil dikonfirmasi
- **THEN** status properti berubah menjadi "dipesan" sehingga tidak dapat dipesan ulang oleh pengguna lain

### Requirement: Dokumen Reservasi Properti

The system MUST mencatat setiap reservasi dalam dokumen yang memiliki nomor referensi, properti, klien, tanggal transaksi, nilai booking fee yang dibayar, relasi transaksi pembayaran, dan status reservasi.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Membuat reservasi

- **WHEN** agen properti membuat dokumen reservasi untuk sebuah properti dan klien
- **THEN** sistem menyimpan dokumen reservasi dalam status `draft` beserta informasi properti, klien, tanggal transaksi, dan pembayaran awalnya

### Requirement: Relasi Reservasi dan Jadwal Pembiayaan

The system MUST menghubungkan dokumen reservasi dengan daftar reservasi pada properti terkait dan daftar jadwal pembiayaan milik reservasi tersebut.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Menampilkan relasi reservasi

- **WHEN** sistem membaca dokumen reservasi atau properti yang terkait
- **THEN** sistem menyediakan relasi dua arah antara properti dan reservasinya serta relasi dari reservasi ke jadwal pembiayaannya

### Requirement: Siklus Status Reservasi

The system MUST mendukung status reservasi `draft`, `waiting_payment`, `confirmed`, dan `canceled`, dengan transisi dari `draft` ke `waiting_payment`, dari `waiting_payment` ke `confirmed`, dan dari `confirmed` ke `canceled`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.3

#### Scenario: Klien menginisiasi pembayaran

- **WHEN** proses pembayaran untuk reservasi diinisiasi
- **THEN** status reservasi berubah dari `draft` menjadi `waiting_payment`

#### Scenario: Pembayaran awal tervalidasi

- **WHEN** sistem pembayaran memvalidasi pembayaran awal
- **THEN** status reservasi berubah dari `waiting_payment` menjadi `confirmed`

#### Scenario: Agen membatalkan reservasi terkonfirmasi

- **WHEN** agen properti membatalkan reservasi yang sudah terkonfirmasi
- **THEN** status reservasi berubah dari `confirmed` menjadi `canceled`

### Requirement: Dokumen Jadwal Cicilan Pembiayaan

The system MUST mencatat setiap jadwal cicilan pembiayaan dalam dokumen yang memiliki relasi dokumen reservasi, keterangan jadwal, tanggal jatuh tempo, nominal tagihan, relasi faktur akuntansi, dan status pembayaran.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Membuat baris jadwal cicilan

- **WHEN** baris jadwal cicilan dibuat untuk sebuah dokumen reservasi
- **THEN** sistem menyimpan data jadwal cicilan yang terhubung ke reservasi tersebut beserta keterangan, tanggal jatuh tempo, nilai tagihan, dan status pembayaran awal `unpaid`

### Requirement: Status Pembayaran Cicilan

The system MUST mendukung pilihan status cicilan `unpaid`, `paid`, dan `late` untuk merefleksikan pemantauan pelunasan tagihan cicilan pembiayaan.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2

#### Scenario: Status awal jadwal cicilan

- **WHEN** sebuah baris jadwal cicilan baru dibuat di dalam sistem
- **THEN** status cicilan bernilai default `unpaid`

### Requirement: Hak Akses Dokumen Reservasi dan Jadwal Cicilan

The system MUST memberikan izin akses CRUD penuh atas dokumen reservasi dan jadwal cicilan kepada Agen Properti, serta izin membaca bagi Klien Portal, sementara Pengunjung Publik tidak memiliki akses ke data tersebut.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Agen properti mengelola dokumen reservasi dan cicilan

- **WHEN** agen properti (pengguna internal) mengakses dokumen reservasi atau jadwal cicilan
- **THEN** sistem mengizinkan hak membaca, membuat, mengubah, dan menghapus dokumen tersebut

#### Scenario: Klien portal mengakses data reservasi dan cicilan

- **WHEN** klien portal mengakses dokumen reservasi atau jadwal cicilan
- **THEN** sistem mengizinkan hak baca serta menolak operasi penulisan, pembuatan, dan penghapusan langsung

### Requirement: Pembatasan Rekaman Dokumen Portal

The system MUST membatasi akses baca pengguna portal hanya pada rekaman reservasi dan jadwal cicilan yang terhubung secara spesifik dengan akun pengguna portal yang bersangkutan.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Klien membaca dokumen reservasi milik sendiri

- **WHEN** klien portal membuka daftar dokumen reservasi atau jadwal cicilan
- **THEN** sistem hanya menampilkan dokumen yang memiliki relasi partner klien sesuai dengan akun pengguna portal tersebut

#### Scenario: Klien mencoba membaca dokumen milik pengguna lain

- **WHEN** klien portal mencoba mengakses dokumen reservasi atau jadwal cicilan milik klien lain
- **THEN** sistem memblokir akses dan tidak menampilkan dokumen tersebut



