## 1. Customer Invoice Generation and State Synchronization

- [x] 1.1 Implementasikan method `action_create_invoice()` pada model `estate.installment` (`addons/estate_booking/models/estate_installment.py`) untuk menerbitkan dokumen draf `account.move` bertipe `out_invoice` dengan rincian partner, nominal, tanggal jatuh tempo, dan baris tagihan yang valid.
- [x] 1.2 Implementasikan method navigasi `action_view_invoice()` pada `estate.installment` untuk memudahkan staf mengakses formulir faktur yang bersangkutan secara langsung.
- [x] 1.3 Implementasikan logika sinkronisasi status `state` pada `estate.installment` untuk memperbarui status menjadi `paid` saat faktur lunas atau `late` jika tanggal jatuh tempo terlewati tanpa pelunasan.

## 2. Scheduled Automation (Cron Job) Setup

- [x] 2.1 Implementasikan method `_cron_generate_due_installment_invoices()` pada `estate.installment` untuk memindai dan menerbitkan draf faktur bagi seluruh cicilan jatuh tempo (`due_date <= context_today`) yang belum memiliki faktur.
- [x] 2.2 Buat file data `addons/estate_booking/data/estate_installment_cron.xml` yang mendefinisikan record `ir.cron` untuk eksekusi pemindaian faktur harian.
- [x] 2.3 Daftarkan file data `data/estate_installment_cron.xml` ke dalam manifest modul `addons/estate_booking/__manifest__.py`.

## 3. Backend User Interface Updates

- [x] 3.1 Perbarui tampilan form view `addons/estate_booking/views/estate_installment_views.xml` dengan menambahkan header form, statusbar status cicilan, tombol aksi "Terbitkan Faktur", dan smart button tautan faktur.
- [x] 3.2 Perbarui tampilan tree view `estate_installment_views.xml` agar status faktur dan relasi dokumen penagihan disajikan secara jelas dan informatif.

## 4. Verification and End-to-End Testing

- [x] 4.1 Jalankan static analysis, validasi sintaks Python (AST check & import integrity), serta validasi XML schema (`xmllint`) pada seluruh file modul yang dibuat atau dimodifikasi.
- [x] 4.2 Uji coba alur integrasi end-to-end: verifikasi pembentukan draf faktur, proteksi pencegahan faktur duplikat, simulasi eksekusi cron job harian, dan verifikasi sinkronisasi status cicilan.
