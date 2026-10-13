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

