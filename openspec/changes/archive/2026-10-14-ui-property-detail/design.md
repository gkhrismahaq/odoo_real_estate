## Context

Halaman katalog publik `/properties` telah berhasil diimplementasikan dan memuat tautan menuju `/property/<id>`. Untuk melanjutkan alur bisnis calon pembeli sesuai TSD Bagian 2.2, sistem memerlukan rute controller detail dan template antarmuka QWeb untuk menyajikan informasi mendalam dari properti terkait.
Lihat `proposal.md` untuk rincian kebutuhan bisnis.

## Goals / Non-Goals

**Goals:**
- Menambahkan method controller `property_detail` pada `PropertyCatalogController` di `addons/estate_booking/controllers/main.py` untuk menangani rute `/property/<int:property_id>`.
- Melakukan verifikasi ketersediaan unit: jika unit tidak berstatus `new` atau tidak aktif, controller mengalihkan pengunjung secara aman ke `/properties`.
- Membuat berkas template QWeb `addons/estate_booking/views/portal_property_detail_templates.xml` yang mewarisi `website.layout`.
- Merancang tata letak modern 2-kolom (area spesifikasi & deskripsi di kolom utama, serta kartu ringkasan harga, booking fee, dan tombol "Book Now" di kolom samping).
- Menyajikan breadcrumb navigasi (Beranda > Katalog Properti > [Nama Properti]).
- Menyajikan rincian teknis lengkap (kamar tidur, luas bangunan, luas taman, garasi, orientasi taman, fasad, tanggal ketersediaan, kode pos).
- Menghubungkan tombol "Book Now" ke rute inisiasi checkout `/booking/checkout?property_id=<id>`.
- Mendaftarkan berkas template XML pada deklarasi `data` di `addons/estate_booking/__manifest__.py`.

**Non-Goals:**
- Pemrosesan form checkout pendaftaran identitas atau transaksi gateway pembayaran (dikelola pada change `ui-booking-checkout`).
- Modifikasi model backend `estate.property`.

## Decisions

### 1. Pola Routing Menggunakan `<int:property_id>` dengan Pengecekan Aman
- **Rationale:** Mengambil ID melalui integer parameter dan membaca rekaman via `request.env['estate.property'].sudo().browse(property_id)` memberikan kendali penuh dalam memvalidasi ketersediaan unit. Jika record tidak ditemukan, tidak aktif, atau statusnya bukan `new`, sistem dapat mengalihkan pengunjung kembali ke katalog dengan aman tanpa memicu crash HTTP 403/404 generik.
- **Alternatives Considered:** Menggunakan route converter bawaan `<model("estate.property"):property>` (berisiko error hak akses record rules publik atau pesan crash yang kurang ramah pengguna).

### 2. Tata Letak 2-Kolom Berbasis Bootstrap 5 (Konten & Sticky Booking Card)
- **Rationale:** Menempatkan spesifikasi dan deskripsi di kolom kiri (`col-lg-8`) dan kartu harga beserta tombol aksi "Book Now" di kolom kanan (`col-lg-4`) mengikuti pola umum situs listing properti modern. Posisi tombol pemesanan tetap menonjol dan mudah diakses pengguna saat membaca rincian unit.
- **Alternatives Considered:** Tata letak 1 kolom vertikal memanjang (menempatkan tombol aksi di bagian terbawah yang rentan terlewat oleh pengguna).

### 3. Pemformatan Nilai Finansial Terpadu dengan Mata Uang Perusahaan
- **Rationale:** Seluruh representasi moneter (`expected_price` dan `booking_fee`) diformat menggunakan widget `monetary` dengan referensi `website.company_id.currency_id` untuk memastikan kepatuhan penuh terhadap standar multi-currency Odoo 17.
- **Alternatives Considered:** Pemformatan string hardcoded (tidak fleksibel dan melanggar prinsip enterprise-level).

## Risks / Trade-offs

- [Risk: Pengunjung mengakses properti yang statusnya telah dipesan atau terjual] → Controller secara ketat mengevaluasi `property.status == 'new'` sebelum merender halaman. Jika tidak memenuhi syarat, pengunjung dialihkan kembali ke katalog `/properties`.
- [Risk: Link checkout "Book Now" belum memiliki controller penerima sebelum change checkout selesai] → Tombol mengarahkan ke `/booking/checkout?property_id=...` yang merupakan target antarmuka pada change berikutnya (`ui-booking-checkout`).
