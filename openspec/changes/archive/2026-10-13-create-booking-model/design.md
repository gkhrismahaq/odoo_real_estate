## Context

Lihat alasan perubahan pada `proposal.md`. Modul `estate_booking` telah memperluas `estate.property` dengan `booking_fee` dan pilihan status `reserved`, tetapi belum memiliki model `estate.booking`; relasi `booking_ids` yang ditetapkan pada spesifikasi utama juga belum ada pada kode. Model dasar `estate.property` memakai nilai harga bertipe `Float` dan tidak mendefinisikan mata uang. TSD menetapkan `booking_fee_paid` sebagai nilai Monetary serta menetapkan relasi transaksi pembayaran dan cicilan, sedangkan implementasi model cicilan dan integrasi pembayaran dijadwalkan sebagai change berikutnya.

## Goals / Non-Goals

**Goals:**

- Menambahkan satu model Odoo `estate.booking` dengan seluruh field dan pilihan status yang ditetapkan TSD.
- Menyediakan relasi dua arah antara `estate.property` dan `estate.booking` tanpa mengubah field properti yang telah ada.
- Menyediakan tindakan model untuk transisi status yang ditetapkan TSD sebagai titik integrasi bagi change pembayaran selanjutnya.
- Menyediakan field mata uang teknis yang diperlukan oleh nilai `Monetary` tanpa menambah aturan bisnis mata uang baru.

**Non-Goals:**

- Membuat model `estate.installment` atau menghasilkan jadwal cicilan.
- Membuat `payment.transaction`, memproses webhook, atau mengubah status properti menjadi `reserved` secara otomatis.
- Membuat hak akses, record rule, menu, atau view backend dan portal.
- Menetapkan kebijakan pembatalan tambahan selain transisi yang ditentukan TSD.

## Decisions

### 1. Model reservasi mandiri dengan relasi Odoo standar

- **Rationale:** `estate.booking` akan menjadi model mandiri yang menyimpan `Many2one` ke `estate.property`, `res.partner`, dan `payment.transaction`, serta `One2many` ke `estate.installment`. Perluasan `estate.property` akan menambahkan `booking_ids` sebagai `One2many` dengan inverse `property_id`. Struktur ini tepat mencerminkan daftar field dan relasi pada TSD serta memenuhi relasi balik yang sudah ditetapkan di spesifikasi capability.
- **Alternatives Considered:** Menyimpan data reservasi langsung sebagai field pada `estate.property`; ditolak karena TSD secara eksplisit menetapkan model baru `estate.booking` dan properti perlu menyimpan daftar reservasi.

### 2. Monetary memakai mata uang perusahaan aktif

- **Rationale:** `booking_fee_paid` akan memakai `fields.Monetary` sesuai TSD. Model akan menyediakan `currency_id` sebagai field teknis dengan nilai awal mata uang perusahaan aktif agar field Monetary memiliki mata uang tanpa mengubah model `estate.property` atau membuat kebijakan mata uang tersendiri.
- **Alternatives Considered:** Mengubah `booking_fee_paid` menjadi `Float`; ditolak karena bertentangan dengan tipe Monetary pada TSD. Menambah mata uang pada `estate.property`; ditolak karena berada di luar change ini.

### 3. Status awal dan tindakan transisi terbatas

- **Rationale:** Field `state` akan memakai pilihan dan nilai awal `draft` yang ditetapkan TSD. Tindakan transisi hanya akan mendukung urutan `draft` → `waiting_payment` → `confirmed` → `canceled`; perubahan status properti dan pemanggilan dari payment gateway akan ditangani change `automate-state-transitions` dan `webhook-payment-callback` sesuai roadmap.
- **Alternatives Considered:** Membuat transisi bebas antarsemua status; ditolak karena tidak mencerminkan siklus status pada TSD. Mengimplementasikan integrasi pembayaran sekarang; ditolak karena sudah dialokasikan ke change lain pada roadmap.

## Risks / Trade-offs

- Model `estate.installment` belum tersedia ketika relasi `installment_ids` dideklarasikan → Change `create-installment-model` harus menambahkan model tersebut sebelum pembaruan modul yang memuat relasi dipasang pada database; implementasi perlu diverifikasi pada registry Odoo.
- Model `payment.transaction` berasal dari dependensi `payment` → Implementasi harus memakai nama model teknis yang tersedia pada Odoo 17 dan tidak membuat model transaksi baru.
- Konfirmasi reservasi belum otomatis mereservasi properti → Batas ini disengaja; otomatisasi hanya dimulai setelah callback pembayaran dan state-transition change dilaksanakan.

## Migration Plan

1. Tambahkan dan daftarkan model `estate.booking` serta relasi balik pada perluasan `estate.property`.
2. Perbarui modul `estate_booking` pada database target agar tabel dan kolom baru dibuat oleh ORM Odoo.
3. Jika perlu rollback sebelum data reservasi dipakai, kembalikan deployment modul ke revisi sebelumnya dan lakukan pemulihan database sesuai prosedur operasional; tidak ada migrasi data lama karena model ini baru.
