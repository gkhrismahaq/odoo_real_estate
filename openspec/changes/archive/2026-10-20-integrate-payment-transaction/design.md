## Context

Saat ini, modul `estate_booking` telah memiliki model reservasi `estate.booking` dengan field `payment_transaction_id` (`Many2one` ke `payment.transaction`) serta transisi status `draft` ke `waiting_payment` (`action_waiting_payment()`). Pengguna telah dapat mengisi formulir pemesanan dan diterbitkan dokumen draf reservasi melalui rute `/booking/checkout/submit` yang berlanjut ke `/booking/confirmation/<id>`.

Sesuai dengan SSOT TSD (Bagian 1.3, 2.2, 3.1, 3.2, 3.3) dan Roadmap Fase 4 (Bagian 4.1), modul `payment` Odoo telah didaftarkan sebagai dependensi modul. Langkah berikutnya adalah membangun integrasi teknis antara dokumen reservasi dengan Payment Engine Odoo untuk menghasilkan rekaman transaksi pembayaran `payment.transaction`, mengarahkan pengguna ke Test Provider, dan mengalihkan status reservasi ke `waiting_payment`.
Lihat `proposal.md` untuk rincian latar belakang bisnis.

## Goals / Non-Goals

**Goals:**
- Mengembangkan model ekstensi `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`) dengan field `booking_id = fields.Many2one("estate.booking")` guna mendukung relasi dua arah yang bersih.
- Menambahkan business method `_create_or_get_payment_transaction(provider_id=None)` pada model `estate.booking` untuk menginisiasi rekaman `payment.transaction` dengan nilai nominal sesuai `booking_fee_paid` dan mata uang dokumen booking.
- Mengotomatisasi transisi status `estate.booking` dari `draft` ke `waiting_payment` saat transaksi pembayaran diinisiasi.
- Menyediakan rute GET `/booking/pay/<int:booking_id>` pada controller `addons/estate_booking/controllers/main.py` untuk menyajikan antarmuka pembayaran digital dengan Payment Provider aktif (khususnya *Test Provider*).
- Membuat template QWeb `addons/estate_booking/views/portal_booking_payment_templates.xml` yang menampilkan rincian tagihan uang tanda jadi dan antarmuka pemrosesan pembayaran Odoo.
- Memperbarui template konfirmasi reservasi (`addons/estate_booking/views/portal_booking_checkout_templates.xml`) dengan tombol utama "Lanjutkan ke Pembayaran" menuju `/booking/pay/<booking_id>`.
- Mendaftarkan model baru dan template baru pada `__manifest__.py` serta file init terkait.

**Non-Goals:**
- Pemrosesan sinyal balik webhook notifikasi pembayaran dari pihak ketiga (ditangani pada change berikutnya: `webhook-payment-callback`).
- Otomatisasi pengubahan status unit properti menjadi `reserved` dan booking menjadi `confirmed` pasca-pembayaran berhasil (ditangani pada change: `automate-state-transitions`).
- Integrasi penerbitan jadwal cicilan dan draf faktur akuntansi `account.move` (ditangani pada Fase 5).

## Decisions

### 1. Pola Relasi Dua Arah antara `estate.booking` dan `payment.transaction`
- **Rationale:** Model `estate.booking` telah memiliki field `payment_transaction_id`. Dengan menambahkan relasi balik `booking_id` pada model ekstensi `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`), arsitektur modul mengikuti konvensi native Odoo (sebagaimana modul `sale` atau `website_sale` mengaitkan `order_id` pada `payment.transaction`). Hal ini mempermudah pelacakan dokumen booking dari transaksi dan sebaliknya, serta menyederhanakan pemrosesan callback webhook di masa mendatang.
- **Alternatives Considered:** Hanya mengandalkan `payment_transaction_id` satu arah pada `estate.booking` tanpa field relasi pada `payment.transaction` (menyulitkan query balik dan penanganan callback asinkron dari payment gateway).

### 2. Enkapsulasi Pembuatan Transaksi pada Model Layer (Clean Architecture)
- **Rationale:** Seluruh logika validasi nominal, penentuan mata uang, pengecekan transaksi eksisting (idempotency), dan transisi status `action_waiting_payment()` dienkapsulasi di dalam method model `estate.booking._create_or_get_payment_transaction()`. Controller hanya bertindak sebagai presentation/orchestration layer yang memanggil method model via `sudo()`. Hal ini mencegah duplikasi logika bisnis dan menjaga kemudahan pengujian (*testability*).
- **Alternatives Considered:** Menempatkan logika pembuatan `payment.transaction` langsung di dalam method rute controller (melanggar prinsip *Separation of Concerns* dan menyulitkan penggunaan kembali).

### 3. Pemanfaatan Provider Bawaan Odoo (*Test Provider*) untuk Lingkungan Sandbox
- **Rationale:** Modul `payment` Odoo 17 menyediakan provider `Test` (demo) yang memungkinkan simulasi pembayaran berhasil (*done*) atau tertunda (*pending*) tanpa memerlukan akun merchant riil atau dependensi eksternal. Controller akan mencari payment provider yang berstatus `test` atau `enabled` untuk disajikan pada formulir pembayaran `/booking/pay/<id>`.
- **Alternatives Considered:** Membangun gateway mock custom dari nol (menyimpang dari standar Odoo dan menyia-nyiakan fitur native payment provider Odoo).

### 4. Idempotensi Transaksi Pembayaran
- **Rationale:** Apabila pengguna merefresh halaman `/booking/pay/<id>` atau kembali ke halaman pembayaran setelah menutup tab, sistem akan mendeteksi rekaman `payment.transaction` yang sedang berjalan (status `draft` atau `pending`) dan menggunakannya kembali alih-alih membuat transaksi baru berulang kali yang mengotori basis data.
- **Alternatives Considered:** Selalu membuat rekaman `payment.transaction` baru setiap kali halaman diakses (menghasilkan banyak transaksi duplikat yatim/orphan).

## Risks / Trade-offs

- [Risk: Calon pembeli mengakses halaman pembayaran untuk booking yang sudah dibatalkan atau sudah lunas] → Controller melakukan pengecekan status dokumen booking (`state in ('draft', 'waiting_payment')`). Jika status bukan tahap pembayaran yang valid, pengguna dialihkan ke halaman konfirmasi booking atau katalog properti dengan pesan informasi yang sesuai.
- [Risk: Tidak ada Payment Provider yang aktif di lingkungan Odoo] → Controller dan template menangani kondisi fallback jika provider aktif belum terkonfigurasi dengan menampilkan pesan ramah bagi pengguna dan petunjuk aktivasi Test Provider bagi administrator.
- [Risk: Nilai nominal uang tanda jadi tidak valid atau bernilai nol] → Model memvalidasi `booking_fee_paid > 0` sebelum membuat rekaman transaksi pembayaran untuk mencegah penerbitan transaksi kosong.
