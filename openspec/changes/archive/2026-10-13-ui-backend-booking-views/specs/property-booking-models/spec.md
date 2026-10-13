## ADDED Requirements

### Requirement: Antarmuka Tampilan Manajemen Reservasi Properti

The system MUST menyediakan antarmuka Tree/List view, Form view dengan kontrol statusbar dan tombol transisi alur kerja, Search filter, serta integrasi navigasi menu backend untuk mengelola dokumen reservasi properti.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Menampilkan daftar reservasi properti

- **WHEN** agen properti membuka menu navigasi Reservasi
- **THEN** sistem menampilkan daftar dokumen reservasi dalam bentuk tree/list view yang memuat referensi, properti, klien, tanggal, nilai pembayaran awal, dan status

#### Scenario: Melihat dan mengelola formulir reservasi properti

- **WHEN** agen properti membuka formulir detail reservasi properti
- **THEN** sistem menyajikan formulir yang menampilkan informasi reservasi, statusbar status, tombol aksi alur transisi status (`action_waiting_payment`, `action_confirm`, `action_cancel`), dan daftar baris jadwal pembiayaan secara terpadu

### Requirement: Antarmuka Tampilan Manajemen Jadwal Cicilan

The system MUST menyediakan antarmuka Tree/List view, Form view, Search filter, serta menu navigasi backend untuk meninjau dan mengelola jadwal cicilan pembiayaan properti.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Menampilkan daftar jadwal cicilan

- **WHEN** pengguna internal membuka menu navigasi Jadwal Cicilan
- **THEN** sistem menyajikan daftar cicilan dalam bentuk tree/list view yang memuat reservasi terkait, keterangan, tanggal jatuh tempo, nominal tagihan, dan status pembayaran

#### Scenario: Membuka formulir jadwal cicilan

- **WHEN** pengguna internal membuka formulir detail jadwal cicilan
- **THEN** sistem menampilkan data detail jadwal cicilan, referensi reservasi, tanggal jatuh tempo, nilai tagihan, faktur terkait, dan status pembayarannya
