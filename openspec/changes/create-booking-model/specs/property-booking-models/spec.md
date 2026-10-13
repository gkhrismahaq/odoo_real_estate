## ADDED Requirements

### Requirement: Dokumen Reservasi Properti

The system MUST mencatat setiap reservasi dalam dokumen yang memiliki nomor referensi, properti, klien, tanggal transaksi, nilai booking fee yang dibayar, relasi transaksi pembayaran, dan status reservasi.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.2.

#### Scenario: Membuat reservasi

- **WHEN** agen properti membuat dokumen reservasi untuk sebuah properti dan klien
- **THEN** sistem menyimpan dokumen reservasi dalam status `draft` beserta informasi properti, klien, tanggal transaksi, dan pembayaran awalnya

### Requirement: Relasi Reservasi dan Jadwal Pembiayaan

The system MUST menghubungkan dokumen reservasi dengan daftar reservasi pada properti terkait dan daftar jadwal pembiayaan milik reservasi tersebut.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.2.

#### Scenario: Menampilkan relasi reservasi

- **WHEN** sistem membaca dokumen reservasi atau properti yang terkait
- **THEN** sistem menyediakan relasi dua arah antara properti dan reservasinya serta relasi dari reservasi ke jadwal pembiayaannya

### Requirement: Siklus Status Reservasi

The system MUST mendukung status reservasi `draft`, `waiting_payment`, `confirmed`, dan `canceled`, dengan transisi dari `draft` ke `waiting_payment`, dari `waiting_payment` ke `confirmed`, dan dari `confirmed` ke `canceled`.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.3.

#### Scenario: Klien menginisiasi pembayaran

- **WHEN** proses pembayaran untuk reservasi diinisiasi
- **THEN** status reservasi berubah dari `draft` menjadi `waiting_payment`

#### Scenario: Pembayaran awal tervalidasi

- **WHEN** sistem pembayaran memvalidasi pembayaran awal
- **THEN** status reservasi berubah dari `waiting_payment` menjadi `confirmed`

#### Scenario: Agen membatalkan reservasi terkonfirmasi

- **WHEN** agen properti membatalkan reservasi yang sudah terkonfirmasi
- **THEN** status reservasi berubah dari `confirmed` menjadi `canceled`
