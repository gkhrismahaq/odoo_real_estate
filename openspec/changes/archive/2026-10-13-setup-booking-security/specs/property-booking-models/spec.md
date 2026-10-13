## ADDED Requirements

### Requirement: Hak Akses Dokumen Reservasi dan Jadwal Cicilan

The system MUST memberikan izin akses CRUD penuh atas dokumen reservasi dan jadwal cicilan kepada Agen Properti, serta izin membaca bagi Klien Portal, sementara Pengunjung Publik tidak memiliki akses ke data tersebut.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Agen properti mengelola dokumen reservasi dan cicilan

- **WHEN** agen properti (pengguna internal) mengakses dokumen reservasi atau jadwal cicilan
- **THEN** sistem mengizinkan hak membaca, membuat, mengubah, dan menghapus dokumen tersebut

#### Scenario: Klien portal mengakses data reservasi dan cicilan

- **WHEN** klien portal mengakses dokumen reservasi atau jadwal cicilan
- **THEN** sistem mengizinkan hak baca serta menolak operasi penulisan, pembuatan, dan penghapusan langsung

### Requirement: Pembatasan Rekaman Dokumen Portal

The system MUST membatasi akses baca pengguna portal hanya pada rekaman reservasi dan jadwal cicilan yang terhubung secara spesifik dengan akun pengguna portal yang bersangkutan.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 3.4.

#### Scenario: Klien membaca dokumen reservasi milik sendiri

- **WHEN** klien portal membuka daftar dokumen reservasi atau jadwal cicilan
- **THEN** sistem hanya menampilkan dokumen yang memiliki relasi partner klien sesuai dengan akun pengguna portal tersebut

#### Scenario: Klien mencoba membaca dokumen milik pengguna lain

- **WHEN** klien portal mencoba mengakses dokumen reservasi atau jadwal cicilan milik klien lain
- **THEN** sistem memblokir akses dan tidak menampilkan dokumen tersebut
