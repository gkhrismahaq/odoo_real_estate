## Context

Lihat alasan dan kebutuhan bisnis pada `proposal.md`. Sistem saat ini telah mampu membentuk baris jadwal cicilan (`estate.installment`) secara otomatis dengan jumlah termin dan nominal angsuran yang terdistribusi presisi. Model `estate.installment` memiliki field relasi pasif `invoice_id` yang mengarah ke `account.move`. Modul `estate_booking` juga telah mencantumkan modul dependensi `account` pada `__manifest__.py`. Change ini merancang arsitektur integrasi aktif untuk menerbitkan dokumen draf *Customer Invoice* (`account.move`), menyediakan otomatisasi penerbitan tagihan terjadwal via cron job Odoo, serta menyinkronkan status pelunasan cicilan dengan modul akuntansi secara konsisten.

## Goals / Non-Goals

**Goals:**

- Mengembangkan method `action_create_invoice()` pada `estate.installment` untuk menerbitkan draf faktur pelanggan (`account.move` bertipe `out_invoice`) lengkap dengan partner pembeli, baris tagihan cicilan, nominal, mata uang, dan tanggal jatuh tempo.
- Menyediakan method navigasi `action_view_invoice()` untuk membuka dokumen faktur terkait dari form view cicilan.
- Mengembangkan cron job harian `_cron_generate_due_installment_invoices()` yang secara otomatis memindai dan menerbitkan draf faktur bagi seluruh cicilan yang telah mencapai atau melewati batas jatuh tempo (`due_date <= context_today`) dan belum memiliki faktur.
- Mengembangkan mekanisme pembaruan/sinkronisasi status cicilan `state` (`unpaid`, `paid`, `late`) berdasarkan status pembayaran faktur (`payment_state` pada `account.move`) dan keterlampauan tanggal jatuh tempo.
- Memperbarui tampilan form dan tree view `estate_installment_views.xml` dengan menambahkan header statusbar, tombol aksi penerbitan faktur, dan smart button tautan faktur.
- Mendaftarkan file data `estate_installment_cron.xml` pada `__manifest__.py`.

**Non-Goals:**

- Menyediakan antarmuka portal klien kustom `/my/invoices` (dialokasikan ke change selanjutnya `ui-customer-portal-invoices`).
- Mengubah alur konfirmasi atau rekonsiliasi pembayaran bawaan modul `account`.

## Decisions

### 1. Pola Konstruksi Dokumen Customer Invoice (`account.move`)

- **Rationale:** Faktur pelanggan diterbitkan dengan tipe `out_invoice` standar Odoo 17. Partner pembeli diambil secara otomatis dari dokumen pemesanan induk (`booking_id.customer_id`). Tanggal faktur (`invoice_date`) ditetapkan hari ini, sedangkan tanggal jatuh tempo (`invoice_date_due`) disinkronkan langsung dengan `due_date` cicilan. Rincian baris faktur (`invoice_line_ids`) memuat nama keterangan cicilan, referensi reservasi, unit properti, serta nominal angsuran `amount` dengan mata uang reservasi.
- **Alternatives Considered:** Menggunakan modul perantara *Sales Order* (`sale.order`); ditolak karena alur bisnis reservasi properti ini langsung mengintegrasikan modul properti dengan modul akuntansi secara ringkas tanpa ketergantungan modul penjualan barang/jasa komersial umum.

### 2. Otomatisasi Terjadwal Harian Berbasis Odoo Scheduled Action (ir.cron)

- **Rationale:** Dibuat record `ir.cron` pada file XML data `addons/estate_booking/data/estate_installment_cron.xml` dengan interval eksekusi 1 hari sekali. Cron mengeksekusi method `_cron_generate_due_installment_invoices()` yang mencari rekaman cicilan berstatus belum lunas yang `due_date <= fields.Date.context_today(self)` dan `invoice_id == False`. Mekanisme ini menjamin tidak ada cicilan jatuh tempo yang terlewatkan dari penagihan.
- **Alternatives Considered:** Mengandalkan pembuatan faktur manual satu per satu oleh staf; ditolak karena rentan kelalaian operasional dan bertentangan dengan mandat otomatisasi sistem pada roadmap.

### 3. Sinkronisasi Dinamis Status Pelunasan Cicilan

- **Rationale:** Status cicilan (`state`) disinkronkan secara reaktif: ketika faktur `invoice_id` terbayar penuh (`payment_state` bernilai `paid` atau `in_payment`), status cicilan diperbarui menjadi `paid`. Apabila cicilan belum lunas dan tanggal jatuh tempo telah lewat (`due_date < context_today`), status cicilan ditandai sebagai `late`. Dengan demikian, status administratif pada modul reservasi mencerminkan status faktual pada buku besar akuntansi.
- **Alternatives Considered:** Mengharuskan pengguna mengubah status cicilan secara manual dari dropdown; ditolak keras karena menciptakan inkonsistensi data antara modul akuntansi dan modul reservasi.

### 4. Proteksi Idempotensi Penerbitan Faktur

- **Rationale:** Method `action_create_invoice()` memvalidasi keberadaan `invoice_id`. Jika rekaman cicilan telah memiliki relasi faktur, sistem menolak pembuatan faktur baru dan melempar `UserError`. Validasi ini menjamin kepatuhan *anti-duplikasi* agar pelanggan tidak menerima penagihan ganda atas satu termin yang sama.
- **Alternatives Considered:** Menimpa faktur yang sudah ada; ditolak karena melanggar integritas jejak audit finansial akuntansi.

## Risks / Trade-offs

- [Risk] Pembuatan faktur gagal jika perusahaan belum mengonfigurasi jurnal penjualan pelanggan (*Sales Journal*). → [Mitigation] Sistem memeriksa keberadaan jurnal bertipe `sale` aktif pada perusahaan, dan memberikan pesan kesalahan deskriptif jika jurnal belum dikonfigurasi.
- [Risk] Penghapusan draf faktur manual oleh admin di modul akuntansi dapat menyebabkan inkonsistensi referensi `invoice_id`. → [Mitigation] Konfigurasikan relasi `invoice_id` dengan penanganan integritas aman (bila faktur dihapus, referensi pada cicilan kembali kosong sehingga dapat diterbitkan ulang jika diperlukan).
