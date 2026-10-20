## Context

Pada change sebelumnya (`integrate-payment-transaction`), rekaman `payment.transaction` telah berhasil diinisiasi untuk pemesanan unit properti dan terhubung dengan dokumen reservasi `estate.booking`. Pengguna diarahkan ke antarmuka pembayaran yang memuat Test Provider Odoo.

Sesuai SSOT TSD (Bagian 1.3, 2.2, 3.2, 3.3) dan Roadmap Fase 4 (Bagian 4.1), tahap selanjutnya adalah menangkap sinyal umpan balik (*webhook* / *callback notification*) dari Payment Gateway (termasuk Test Provider Odoo) melalui metode standar Odoo `_process_notification_data()` pada model `payment.transaction`. Logika ini bertugas memvalidasi keberhasilan pembayaran dan menjamin integritas nominal pembayaran sebelum transisi otomatis status reservasi dan unit properti dieksekusi pada change berikutnya.
Lihat `proposal.md` untuk latar belakang bisnis.

## Goals / Non-Goals

**Goals:**
- Meng-*override* metode `_process_notification_data(self, notification_data)` pada model `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`) untuk menangani umpan balik notifikasi pembayaran dari gateway.
- Memvalidasi integritas data transaksi: memastikan nominal pembayaran (`amount`) dan mata uang (`currency_id`) yang terverifikasi sesuai dengan nilai tagihan tanda jadi (`booking_fee_paid`) pada dokumen `estate.booking`.
- Memastikan pencatatan status transaksi (`done`, `pending`, `cancel`, `error`) terdokumentasi dengan baik pada rekaman transaksi.
- Memperbarui antarmuka web portal pembayaran (`addons/estate_booking/views/portal_booking_payment_templates.xml`) dan controller (`addons/estate_booking/controllers/main.py`) untuk menyajikan kartu status transaksi real-time (Sukses, Menunggu Verifikasi, atau Gagal) saat pengguna kembali ke halaman portal setelah menyelesaikan pembayaran.

**Non-Goals:**
- Otomatisasi pengubahan status unit properti menjadi `reserved` dan booking menjadi `confirmed` (ditangani secara spesifik pada change berikutnya: `automate-state-transitions`).
- Penagihan jadwal cicilan dan penerbitan faktur berkala `account.move` (ditangani pada Fase 5).

## Decisions

### 1. Ekstensi Terkontrol pada Metode Standar `_process_notification_data()`
- **Rationale:** Odoo 17 memproses seluruh notifikasi pembayaran eksternal melalui alur `_handle_notification_data()` yang mendelegasikan pemrosesan payload ke `_process_notification_data(notification_data)`. Dengan meng-*override* metode ini dan memanggil `super()`, kita memanfaatkan mekanisme parsing bawaan provider Odoo secara utuh, sembari menyisipkan validasi integritas khusus pemesanan properti untuk transaksi yang memiliki relasi `booking_id`.
- **Alternatives Considered:** Membuat webhook HTTP endpoint custom sendiri yang memotong alur native Odoo `payment` (melanggar Hard Technical Constraint #4 pada `config.yaml` dan berisiko merusak kompatibilitas provider).

### 2. Validasi Integritas Nominal (*Amount Tampering Prevention*)
- **Rationale:** Pembayaran digital rentan terhadap modifikasi nilai payload atau kesalahan konversi mata uang. Sistem memverifikasi bahwa `self.amount` sama dengan `self.booking_id.booking_fee_paid`. Apabila terjadi perbedaan nominal, transaksi dicegah untuk diselesaikan sebagai transaksi sukses dan ditandai dengan galat anomali nominal (*mismatch error*).
- **Alternatives Considered:** Mengasumsikan seluruh callback yang berstatus sukses selalu membawa nominal yang benar tanpa verifikasi silang terhadap dokumen reservasi.

### 3. Penyajian Status Transaksi Real-time pada Portal
- **Rationale:** Setelah pembeli menyelesaikan interaksi dengan Payment Provider (misalnya menekan tombol sukses pada Test Provider), pengguna diarahkan kembali ke portal pemesanan. Controller mendeteksi status terkini `payment_transaction_id.state` dan template merender kartu status visual yang informatif (sukses berwarna hijau, pending berwarna kuning, atau gagal berwarna merah) dengan petunjuk langkah berikutnya.
- **Alternatives Considered:** Membiarkan tampilan halaman pembayaran tidak berubah seperti sebelum bayar, yang dapat membingungkan pembeli apakah transaksi telah berhasil diproses.

## Risks / Trade-offs

- [Risk: Notifikasi webhook dari gateway diterima berulang kali (*duplicate callback webhook*)] → Metode `_process_notification_data()` memanfaatkan sifat idempotensi bawaan Odoo, di mana transaksi yang telah berstatus `done` tidak akan diproses ulang secara destruktif.
- [Risk: Callback diterima sebelum pengguna kembali ke browser] → Status transaksi tersimpan secara persisten pada basis data PostgreSQL, sehingga saat pengguna memuat ulang halaman pembayaran `/booking/pay/<id>`, sistem langsung menyajikan status mutakhir yang valid.
