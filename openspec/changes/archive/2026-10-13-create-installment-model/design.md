## Context

Lihat alasan perubahan pada `proposal.md`. Model `estate.booking` telah memiliki deklarasi relasi `installment_ids = fields.One2many("estate.installment", "booking_id", string="Jadwal Pembiayaan")`. Pada change ini, model baru `estate.installment` dibuat untuk menyediakan comodel yang valid beserta inverse field `booking_id`, sehingga menyelesaikan kendala resolusi skema pada registry ORM Odoo 17. Sesuai TSD Bagian 3.2, model ini menyimpan informasi relasi reservasi, keterangan jadwal, tanggal jatuh tempo, nominal tagihan, relasi faktur akuntansi, dan status pembayaran.

## Goals / Non-Goals

**Goals:**

- Membuat model data Odoo baru `estate.installment` dengan seluruh field yang ditetapkan pada TSD Bagian 3.2.
- Menyediakan relasi `Many2one` ke `estate.booking` (`booking_id`) sebagai inverse relasi `installment_ids`.
- Menyediakan mata uang teknis `currency_id` yang terhubung dengan dokumen reservasi (`booking_id.currency_id`) agar field `amount` bertipe Monetary berfungsi secara presisi.
- Menyediakan relasi pasif ke `account.move` (`invoice_id`) untuk persiapan integrasi akuntansi.
- Menyediakan field status `state` dengan opsi `unpaid`, `paid`, dan `late` serta nilai awal `unpaid`.
- Memulihkan stabilitas registry Odoo 17 sehingga web server dapat memuat skema tanpa error 500.

**Non-Goals:**

- Mengotomatisasi pembuatan baris jadwal cicilan dari nilai termin pemesanan (dialokasikan ke change `automate-installment-drafts`).
- Menerbitkan faktur pelanggan (`account.move`) secara otomatis (dialokasikan ke change `integrate-customer-invoices`).
- Membuat tampilan antarmuka form/tree backend (dialokasikan ke change `ui-backend-booking-views`).
- Mengonfigurasi hak akses grup dan record rule (dialokasikan ke change `setup-booking-security`).

## Decisions

### 1. Model Mandiri dengan Relasi Inverse ke Reservasi

- **Rationale:** `estate.installment` didefinisikan sebagai model mandiri dengan nama teknis `estate.installment`. Field `booking_id` dikonfigurasi sebagai `fields.Many2one("estate.booking", string="Reservasi", required=True, ondelete="cascade", index=True)`. Konfigurasi `ondelete="cascade"` memastikan integritas data terjamin di mana jadwal cicilan dihapus jika dokumen reservasi induk dihapus. Relasi ini memenuhi inverse field yang diwajibkan oleh relasi `installment_ids` pada `estate.booking`.
- **Alternatives Considered:** Menggunakan `ondelete="restrict"`; ditolak karena entitas cicilan adalah subordinat langsung dari dokumen reservasi sehingga siklus hidupnya terikat penuh.

### 2. Pengelolaan Nilai Monetary dan Sinkronisasi Mata Uang

- **Rationale:** Field `amount` didefinisikan sebagai `fields.Monetary(string="Nilai Tagihan", currency_field="currency_id", required=True)`. Field mata uang teknis `currency_id` dikonfigurasi sebagai `fields.Many2one("res.currency", string="Mata Uang", related="booking_id.currency_id", store=True, readonly=True)` dengan fallback `default=lambda self: self.env.company.currency_id`. Pola ini memastikan nominal tagihan cicilan selalu menggunakan mata uang yang konsisten dengan dokumen reservasi.
- **Alternatives Considered:** Menggunakan tipe `Float`; ditolak karena bertentangan dengan spesifikasi TSD Bagian 3.2 yang mewajibkan `amount (Monetary)`.

### 3. Relasi Faktur Akuntansi Pasif dan Status Cicilan

- **Rationale:** Field `invoice_id` didefinisikan sebagai `fields.Many2one("account.move", string="Faktur Tagihan", readonly=True, copy=False, index=True)` untuk mengaitkan jadwal pembayaran dengan faktur standar Odoo. Field `state` didefinisikan sebagai `fields.Selection(selection=[("unpaid", "Belum Lunas"), ("paid", "Lunas"), ("late", "Terlambat")], string="Status", default="unpaid", required=True, copy=False)`.
- **Alternatives Considered:** Membuat metode transisi status atau otomatisasi update status sekarang; ditolak karena status cicilan akan diperbarui oleh callback rekonsiliasi faktur akuntansi pada change berikutnya.

## Risks / Trade-offs

- Konfigurasi hak akses (`ir.model.access.csv`) untuk model `estate.installment` belum tersedia pada change ini → Dimonitor sebagai trade-off yang disengaja; hak akses grup portal dan internal akan dikonfigurasi secara komprehensif pada change `setup-booking-security`.
- Tampilan backend belum dibuat → Model dapat diuji dan diverifikasi langsung melalui ORM dan shell Odoo sampai change `ui-backend-booking-views` dijalankan.

## Migration Plan

1. Buat file model `estate_installment.py` dan daftarkan di `addons/estate_booking/models/__init__.py`.
2. Jalankan pembaruan modul `estate_booking` agar tabel `estate_installment` dan relasi basis data terbentuk.
3. Muat ulang server Odoo dan pastikan web endpoint `http://localhost:8069/` merespons dengan normal (status 200).
