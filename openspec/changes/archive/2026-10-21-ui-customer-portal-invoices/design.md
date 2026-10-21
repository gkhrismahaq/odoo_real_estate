## Context

Lihat alasan dan kebutuhan bisnis pada `proposal.md`. Sistem saat ini telah mampu meng-generate deretan draf jadwal cicilan (`estate.installment`) dan menerbitkan draf faktur pelanggan (`account.move`). Model data telah diproteksi dengan aturan hak akses portal pada `security.xml` dan `ir.model.access.csv`. Namun, portal pelanggan bawaan Odoo (`/my`) belum memiliki menu atau tampilan untuk menampilkan data reservasi properti dan jadwal cicilannya kepada klien yang bersangkutan. Change ini merancang antarmuka frontend portal pelanggan Odoo 17 yang menyajikan riwayat reservasi properti, transparansi jadwal termin cicilan, dan navigasi langsung menuju faktur pembayaran online.

## Goals / Non-Goals

**Goals:**

- Mengembangkan controller portal `EstateBookingPortal` yang mewarisi `CustomerPortal` pada `addons/estate_booking/controllers/portal.py`.
- Menginjeksi counter dokumen reservasi aktif (`booking_count`) pada beranda portal pelanggan (`/my` dan `/my/home`).
- Menyediakan rute web `/my/bookings` untuk menampilkan daftar riwayat pemesanan properti milik klien login.
- Menyediakan rute web `/my/bookings/<int:booking_id>` untuk menampilkan informasi lengkap unit, pembayaran uang tanda jadi, dan tabel jadwal cicilan pembiayaan.
- Menyediakan tautan langsung dari baris cicilan yang telah berfaktur ke antarmuka resmi faktur Odoo (`/my/invoices/<invoice_id>`).
- Mengembangkan template QWeb responsif pada `addons/estate_booking/views/portal_estate_booking_templates.xml`.
- Menjamin kepatuhan keamanan data dengan membatasi query hanya pada data yang terhubung dengan `request.env.user.partner_id`.

**Non-Goals:**

- Memodifikasi alur checkout publik `/booking/checkout` (sudah selesai pada Fase 3).
- Mengubah alur validasi webhook gateway pembayaran (sudah selesai pada Fase 4).

## Decisions

### 1. Ekstensi Standar Controller Portal Odoo (`CustomerPortal`)

- **Rationale:** Mengembangkan controller portal yang mewarisi `odoo.addons.portal.controllers.portal.CustomerPortal`. Method `_prepare_home_portal_values()` di-override untuk menghitung jumlah pemesanan milik klien (`request.env.user.partner_id`). Hal ini memastikan kartu menu baru "Reservasi Properti" otomatis muncul secara serasi pada beranda portal `/my/home` berdampingan dengan menu bawaan Odoo seperti Faktur dan Pembayaran.
- **Alternatives Considered:** Menggunakan controller terpisah tanpa mewarisi `CustomerPortal`; ditolak karena klien tidak akan mendapatkan pengalaman terintegrasi pada dasbor portal Odoo.

### 2. Proteksi Hak Akses Domain Klien (Anti-IDOR)

- **Rationale:** Setiap pencarian data dokumen pemesanan (`estate.booking`) dan jadwal cicilan (`estate.installment`) menerapkan domain eksplisit `[('customer_id', '=', partner.id)]`. Pada akses rute detail `/my/bookings/<id>`, sistem memvalidasi kepemilikan dokumen. Jika dokumen tidak ditemukan atau milik pengguna lain, sistem mengalihkan pengguna kembali ke `/my/bookings` secara aman.
- **Alternatives Considered:** Membuka akses publik atau bypass filter; ditolak karena melanggar prinsip keamanan data dan privasi klien.

### 3. Komponen Antarmuka Tabel Cicilan dan Penautan Faktur

- **Rationale:** Pada halaman detail pemesanan `/my/bookings/<id>`, tabel jadwal cicilan menyajikan kolom nomor termin, tanggal jatuh tempo, jumlah tagihan, badge status pelunasan (`Belum Lunas`, `Lunas`, `Terlambat`), dan aksi faktur. Apabila cicilan telah memiliki `invoice_id`, sistem menyediakan tombol tautan yang mengarahkan klien langsung ke `/my/invoices/{invoice_id.id}` untuk memudahkan peninjauan dan pembayaran online via payment provider aktif.
- **Alternatives Considered:** Mengharuskan klien mencari nomor faktur secara manual di menu invoices terpisah; ditolak karena menyulitkan pengguna (*poor user experience*).

## Risks / Trade-offs

- [Risk] Klien yang mengakses portal saat koneksi lambat mengalami keterlambatan render halaman riwayat. → [Mitigation] Terapkan sorting terindeks (`booking_date desc, id desc`) dan paginasi standar portal Odoo.
- [Risk] Tampilan tidak proporsional pada perangkat seluler. → [Mitigation] Manfaatkan kelas tabel responsif Bootstrap 5 bawaan Odoo 17 (`table-responsive`, `badge`, `d-flex`).
