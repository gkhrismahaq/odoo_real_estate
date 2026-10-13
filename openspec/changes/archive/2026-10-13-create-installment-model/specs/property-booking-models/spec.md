## ADDED Requirements

### Requirement: Dokumen Jadwal Cicilan Pembiayaan

The system MUST mencatat setiap jadwal cicilan pembiayaan dalam dokumen yang memiliki relasi dokumen reservasi, keterangan jadwal, tanggal jatuh tempo, nominal tagihan, relasi faktur akuntansi, dan status pembayaran.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.2.

#### Scenario: Membuat baris jadwal cicilan

- **WHEN** baris jadwal cicilan dibuat untuk sebuah dokumen reservasi
- **THEN** sistem menyimpan data jadwal cicilan yang terhubung ke reservasi tersebut beserta keterangan, tanggal jatuh tempo, nilai tagihan, dan status pembayaran awal `unpaid`

### Requirement: Status Pembayaran Cicilan

The system MUST mendukung pilihan status cicilan `unpaid`, `paid`, dan `late` untuk merefleksikan pemantauan pelunasan tagihan cicilan pembiayaan.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.2.

#### Scenario: Status awal jadwal cicilan

- **WHEN** sebuah baris jadwal cicilan baru dibuat di dalam sistem
- **THEN** status cicilan bernilai default `unpaid`
