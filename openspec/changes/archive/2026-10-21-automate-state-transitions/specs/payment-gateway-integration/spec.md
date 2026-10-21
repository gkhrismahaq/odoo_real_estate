## ADDED Requirements

### Requirement: Otomatisasi Transisi Status Dokumen Pemesanan

The system MUST secara otomatis mengonfirmasi dokumen pemesanan `estate.booking` (mengubah status dari `waiting_payment` menjadi `confirmed`) sesaat setelah transaksi pembayaran terkait dinyatakan berhasil (`done`) oleh sistem pembayaran digital.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.3.
> **Reference:** [Roadmap](../../../../../docs/01-estate_booking/roadmap.md) — Fase 4, Bagian 4.1.

#### Scenario: Transisi otomatis status booking saat pembayaran sukses

- **WHEN** transaksi pembayaran `payment.transaction` berhasil divalidasi dan beralih ke status `done`
- **THEN** sistem secara reaktif mengeksekusi konfirmasi dokumen reservasi `estate.booking` terkait sehingga statusnya berubah menjadi `confirmed`

#### Scenario: Pencegahan konfirmasi ganda pada reservasi

- **WHEN** notifikasi pembayaran berstatus `done` diproses untuk dokumen reservasi yang telah berstatus `confirmed`
- **THEN** sistem mempertahankan status `confirmed` secara idempoten tanpa memicu galat eksekusi

### Requirement: Penguncian Otomatis Status Ketersediaan Unit Properti

The system MUST secara otomatis memperbarui status ketersediaan unit properti `estate.property` menjadi `reserved` (Dipesan) ketika dokumen pemesanan terkait beralih ke status `confirmed`, guna mengunci unit dan mencegah pemesanan ganda pada katalog publik.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2, 3.2, & 3.3.

#### Scenario: Unit properti terkunci otomatis saat reservasi terkonfirmasi

- **WHEN** dokumen pemesanan `estate.booking` berhasil dikonfirmasi ke status `confirmed`
- **THEN** status unit properti `estate.property` yang bersangkutan secara otomatis diperbarui dari `new` menjadi `reserved`

#### Scenario: Pemulihan status ketersediaan unit saat reservasi dibatalkan

- **WHEN** agen properti membatalkan dokumen pemesanan yang telah terkonfirmasi (`action_cancel`) dan tidak terdapat pemesanan terkonfirmasi aktif lainnya pada unit tersebut
- **THEN** sistem mengembalikan status unit properti menjadi `new` sehingga unit kembali tersedia pada katalog properti
