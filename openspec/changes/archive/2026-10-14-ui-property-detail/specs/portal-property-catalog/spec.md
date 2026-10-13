## ADDED Requirements

### Requirement: Akses Rute Halaman Rincian Properti Publik

The system MUST menyediakan rute web publik `/property/<id>` yang menyajikan informasi detail komprehensif dari unit properti yang berstatus baru bagi pengunjung umum.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2.

#### Scenario: Pengunjung mengakses rincian properti berstatus baru

- **WHEN** pengunjung membuka URL rincian properti yang berstatus `new` dan aktif
- **THEN** sistem menyajikan halaman web rincian properti dengan status HTTP 200 lengkap dengan deskripsi, spesifikasi, dan biaya pemesanan

#### Scenario: Pengunjung mengakses properti yang tidak tersedia

- **WHEN** pengunjung membuka URL rincian properti yang tidak berstatus `new` atau tidak aktif
- **THEN** sistem mengalihkan pengunjung kembali ke halaman katalog `/properties` dengan pesan informasi bahwa unit tidak tersedia

### Requirement: Penyajian Spesifikasi Lengkap dan Tombol Pemesanan Unit

The system MUST menyajikan ringkasan harga bukaan, biaya uang tanda jadi (booking fee), tabel spesifikasi fisik unit (kamar tidur, luas bangunan, luas taman, garasi, orientasi taman, tanggal ketersediaan), serta tombol aksi pemesanan ("Book Now") yang mengarahkan pengguna ke alur checkout.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 & 3.2.

#### Scenario: Informasi spesifikasi dan tombol pemesanan ditampilkan

- **WHEN** halaman rincian properti berhasil dimuat
- **THEN** sistem menampilkan rincian harga, booking fee, fasilitas, dan tombol pemesanan "Book Now" yang memuat tautan menuju formulir pemesanan unit terkait
