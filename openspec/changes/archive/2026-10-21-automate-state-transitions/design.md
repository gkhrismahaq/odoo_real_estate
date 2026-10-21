## Context

Pada tahap sebelumnya (`webhook-payment-callback`), transaksi pembayaran `payment.transaction` telah dapat memproses notifikasi dari gateway pembayaran dan memverifikasi integritas nominal uang tanda jadi. Sesuai SSOT TSD (Bagian 2.2 alur #4 & Bagian 3.3) dan Roadmap Fase 4 (Bagian 4.1), tahap ini mengimplementasikan transisi otomatis:
1. Status reservasi `estate.booking` beralih dari `waiting_payment` ke `confirmed`.
2. Status unit properti `estate.property` beralih dari `new` ke `reserved` (Dipesan).
Lihat `proposal.md` untuk latar belakang bisnis.

## Goals / Non-Goals

**Goals:**
- Menyempurnakan method `action_confirm()` pada model `estate.booking` agar secara otomatis memperbarui status unit properti terkait (`property_id.status = 'reserved'`) saat booking terkonfirmasi.
- Menyempurnakan method `action_cancel()` pada model `estate.booking` agar secara cerdas mengembalikan status properti menjadi `new` jika tidak ada booking terkonfirmasi lainnya yang aktif.
- Memperbarui model `payment.transaction` (`addons/estate_booking/models/payment_transaction.py`) agar sesaat setelah transaksi dinyatakan `done`, sistem secara otomatis memicu pemanggilan `tx.booking_id.action_confirm()`.
- Memperbarui template portal konfirmasi dan pembayaran untuk menyajikan status unit terkunci dan pemesanan terkonfirmasi kepada klien secara real-time.

**Non-Goals:**
- Pembuatan jadwal termin tagihan cicilan berkala `estate.installment` (dikelola pada Fase 5).
- Penerbitan otomatis draf faktur akuntansi `account.move` (dikelola pada Fase 5).

## Decisions

### 1. Enkapsulasi Penguncian Status Properti di `estate.booking.action_confirm()`
- **Rationale:** Mengintegrasikan perubahan status `property_id.status = 'reserved'` di dalam method domain `action_confirm()` menjamin konsistensi sistem. Baik pemesanan dikonfirmasi secara otomatis dari sinyal webhook pembayaran maupun dikonfirmasi secara manual oleh staf internal melalui form view backend Odoo, properti akan selalu terkunci secara konsisten.
- **Alternatives Considered:** Mengubah status properti langsung di dalam controller web atau di dalam model transaksi (menyebabkan logika bisnis tersebar/spaghetti dan berisiko terlewat saat dikonfirmasi via backend).

### 2. Pemicu Reaktif Konfirmasi pada `payment.transaction` saat State Menjadi `done`
- **Rationale:** Saat notifikasi pembayaran berhasil diproses pada `payment.transaction._process_notification_data()` atau saat transaksi beralih ke `done`, sistem secara langsung memanggil `tx.booking_id.action_confirm()`. Hal ini mengeksekusi transisi status secara instan (real-time) sehingga tidak ada celah waktu (*race condition*) di mana pengunjung lain dapat memesan unit yang sama.
- **Alternatives Considered:** Menggunakan cron job terjadwal (menghasilkan *delay* beberapa menit dan berisiko terjadinya pemesanan ganda di katalog).

### 3. Pemulihan Otomatis Status Ketersediaan Properti pada Pembatalan (`action_cancel()`)
- **Rationale:** Apabila sebuah reservasi yang telah terkonfirmasi dibatalkan oleh agen properti, sistem mengecek apakah masih terdapat dokumen booking terkonfirmasi lainnya untuk unit tersebut. Jika tidak ada, status properti secara otomatis dikembalikan ke `new` sehingga unit kembali muncul pada katalog publik `/properties`.
- **Alternatives Considered:** Membiarkan properti tetap berstatus `reserved` dan menuntut agen properti mengubah statusnya secara manual ke `new` (rentan kelalaian manusia / human error).

## Risks / Trade-offs

- [Risk: Transaksi pembayaran `done` diterima berulang kali (*duplicate webhook callback*)] → Pengecekan idempotensi pada `action_confirm()` memastikan bahwa jika booking sudah dalam status `confirmed`, sistem tidak akan melempar UserError atau melakukan penulisan ulang yang tidak perlu.
- [Risk: Unit properti sudah tidak lagi berstatus `new` saat pembayaran selesai (misalnya unit telah terjual)] → Model memverifikasi kondisi properti sebelum mengunci status dan mencatat log aktivitas jika terjadi konflik status.
