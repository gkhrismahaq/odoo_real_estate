## ADDED Requirements

### Requirement: Penyajian Menu dan Riwayat Pemesanan pada Portal Pelanggan

The system MUST menyediakan antarmuka web portal pada rute `/my/bookings` dan kartu tautan menu pada beranda portal pelanggan (`/my/home`) yang menyajikan daftar dokumen reservasi milik mitra klien yang sedang login secara aman.
> **Reference:** [Roadmap](../../../../../docs/01-estate_booking/roadmap.md) — Fase 5, Bagian 5.1 (`installment-invoicing`).
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.1 (Profil Pengguna Klien) & Bagian 3.4 (Hak Akses Portal).

#### Scenario: Klien melihat daftar pemesanan properti miliknya di portal

- **WHEN** klien yang telah terautentikasi mengakses halaman `/my/bookings`
- **THEN** sistem menampilkan daftar seluruh dokumen reservasi `estate.booking` yang terikat dengan akun klien tersebut lengkap dengan referensi pemesanan, nama unit properti, tanggal transaksi, dan status terkini

#### Scenario: Pengunjung publik tanpa autentikasi dialihkan ke laman masuk

- **WHEN** pengunjung situs yang belum masuk (belum login) mengakses URL `/my/bookings`
- **THEN** sistem secara otomatis mengalihkan pengguna ke halaman login portal Odoo (`/web/login`)

### Requirement: Transparansi Rincian Jadwal Cicilan pada Halaman Detail Reservasi Portal

The system MUST menyajikan halaman rincian pemesanan pada rute `/my/bookings/<int:booking_id>` yang menampilkan data lengkap properti, rekapitulasi pembayaran uang tanda jadi, sisa kewajiban pembayaran, serta tabel jadwal termin pembiayaan `estate.installment` yang terstruktur.
> **Reference:** [Roadmap](../../../../../docs/01-estate_booking/roadmap.md) — Fase 5, Bagian 5.1 (`installment-invoicing`).
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 (Alur Proses Bisnis butir 5).

#### Scenario: Klien meninjau jadwal cicilan pada dokumen reservasi

- **WHEN** klien membuka halaman rincian reservasi `/my/bookings/<id>` yang valid
- **THEN** sistem menyajikan tabel jadwal cicilan berurutan per tanggal jatuh tempo, nominal per termin, status pelunasan (`unpaid`, `paid`, `late`), dan nomor faktur jika telah diterbitkan

#### Scenario: Pencegahan akses lintas pengguna pada detail reservasi

- **WHEN** klien mencoba membuka URL `/my/bookings/<id>` untuk dokumen pemesanan milik mitra lain
- **THEN** sistem menolak akses, memblokir tampilan data, dan mengalihkan pengguna kembali ke halaman daftar reservasi `/my/bookings` dengan pesan akses tidak diizinkan

### Requirement: Akses dan Navigasi Faktur Cicilan dari Portal Pelanggan

The system MUST menyediakan tautan navigasi langsung dari baris tabel cicilan yang telah memiliki relasi faktur menuju formulir portal faktur pelanggan bawaan Odoo (`/my/invoices/<int:invoice_id>`), memfasilitasi klien untuk meninjau berkas faktur dan menyelesaikan pembayaran secara online.
> **Reference:** [TSD](../../../../../docs/01-estate_booking/tsd.md) — Bagian 1.2 & Bagian 2.2.

#### Scenario: Klien menavigasi ke dokumen faktur dari daftar cicilan portal

- **WHEN** klien mengklik tautan atau tombol "Lihat Faktur" pada baris cicilan yang memiliki `invoice_id`
- **THEN** sistem mengarahkan klien ke antarmuka resmi portal faktur `/my/invoices/<invoice_id>` lengkap dengan opsi pembayaran digital bawaan Odoo

#### Scenario: Penanganan baris cicilan yang belum berfaktur

- **WHEN** baris jadwal cicilan masih berstatus draf administrasi dan belum diterbitkan fakturnya oleh staf keuangan
- **THEN** sistem menampilkan badge keterangan status tanpa menyediakan tautan faktur aktif
