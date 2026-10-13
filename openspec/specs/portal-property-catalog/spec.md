# portal-property-catalog Specification

## Purpose

Menyediakan antarmuka publik web portal bagi calon pembeli dan pengunjung situs untuk menelusuri katalog unit properti yang tersedia untuk dipesan beserta ringkasan spesifikasi dasarnya.

## Requirements

### Requirement: Akses Halaman Katalog Properti Publik

The system MUST menyediakan rute web publik `/properties` yang dapat diakses oleh pengunjung umum tanpa autentikasi login untuk melihat katalog unit properti yang tersedia.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.3 & 2.2.

#### Scenario: Pengunjung mengakses katalog properti

- **WHEN** pengunjung membuka URL `/properties` melalui peramban web
- **THEN** sistem merespons dengan kode HTTP 200 dan menyajikan halaman katalog properti berbasis layout website

### Requirement: Penyaringan Properti Tersedia pada Katalog

The system MUST hanya menampilkan unit properti yang berstatus "Baru" (`new`) dan dalam kondisi aktif pada katalog publik untuk mencegah penawaran unit yang telah dipesan atau terjual.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Menampilkan hanya properti berstatus baru

- **WHEN** halaman katalog properti dimuat
- **THEN** sistem hanya menampilkan kartu properti dengan status `new` dan tidak menyertakan properti yang berstatus `reserved`, `sold`, atau `canceled`

#### Scenario: Katalog saat tidak ada properti berstatus baru

- **WHEN** halaman katalog properti dimuat dan tidak ada rekaman properti yang memenuhi kriteria status `new`
- **THEN** sistem menampilkan pesan informasi ramah bahwa saat ini belum ada unit properti yang tersedia

### Requirement: Kartu Informasi Unit Properti

The system MUST menyajikan kartu unit properti yang memuat informasi nama properti, tipe properti, harga penawaran/bukaan, lokasi atau kode pos, jumlah kamar tidur, dan luas bangunan.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Informasi pada kartu properti

- **WHEN** daftar unit properti dirender pada halaman web
- **THEN** setiap unit disajikan dalam kartu yang memuat nama, tipe, harga, kode pos, jumlah kamar tidur, dan luas bangunan secara informatif

### Requirement: Akses Rute Halaman Rincian Properti Publik

The system MUST menyediakan rute web publik `/property/<id>` yang menyajikan informasi detail komprehensif dari unit properti yang berstatus baru bagi pengunjung umum.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2.

#### Scenario: Pengunjung mengakses rincian properti berstatus baru

- **WHEN** pengunjung membuka URL rincian properti yang berstatus `new` dan aktif
- **THEN** sistem menyajikan halaman web rincian properti dengan status HTTP 200 lengkap dengan deskripsi, spesifikasi, dan biaya pemesanan

#### Scenario: Pengunjung mengakses properti yang tidak tersedia

- **WHEN** pengunjung membuka URL rincian properti yang tidak berstatus `new` atau tidak aktif
- **THEN** sistem mengalihkan pengunjung kembali ke halaman katalog `/properties` dengan pesan informasi bahwa unit tidak tersedia

### Requirement: Penyajian Spesifikasi Lengkap dan Tombol Pemesanan Unit

The system MUST menyajikan ringkasan harga bukaan, biaya uang tanda jadi (booking fee), tabel spesifikasi fisik unit (kamar tidur, luas bangunan, luas taman, garasi, orientasi taman, tanggal ketersediaan), serta tombol aksi pemesanan ("Book Now") yang mengarahkan pengguna ke alur checkout.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Informasi spesifikasi dan tombol pemesanan ditampilkan

- **WHEN** halaman rincian properti berhasil dimuat
- **THEN** sistem menampilkan rincian harga, booking fee, fasilitas, dan tombol pemesanan "Book Now" yang memuat tautan menuju formulir pemesanan unit terkait

