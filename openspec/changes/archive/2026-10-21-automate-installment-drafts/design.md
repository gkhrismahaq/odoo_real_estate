## Context

Lihat alasan dan motivasi perubahan pada `proposal.md`. Sistem saat ini telah memiliki model data `estate.booking` dan `estate.installment`. Saat transaksi pembayaran uang tanda jadi (`payment.transaction`) tervalidasi sukses (`done`), webhook memicu method `action_confirm()` pada `estate.booking` yang mengubah status booking menjadi `confirmed` dan mengunci unit properti menjadi `reserved`. Namun, sistem belum mengotomatisasi pembuatan baris jadwal cicilan (`estate.installment`) dan belum memiliki field pengaturan termin pada dokumen reservasi. Change ini merancang arsitektur pembentukan draf jadwal cicilan otomatis secara reaktif dan aman.

## Goals / Non-Goals

**Goals:**

- Menambahkan field `installment_term` (Integer, default 12) dan compute field `remaining_amount` (Monetary) pada model `estate.booking`.
- Mengembangkan method kalkulasi jadwal cicilan `action_generate_installments()` pada `estate.booking` dengan presisi pembagian merata, penanganan selisih pembulatan mata uang pada termin terakhir, dan penentuan tanggal jatuh tempo bulanan bertahap menggunakan `relativedelta`.
- Mengintegrasikan pembuatan cicilan otomatis ke dalam method `action_confirm()` pada `estate.booking` dengan jaminan idempotensi.
- Menyediakan tombol manual "Buat Jadwal Cicilan" pada tampilan backend form `estate.booking` yang dilengkapi validasi proteksi terhadap baris cicilan yang sudah memiliki keterkaitan faktur (`invoice_id`).
- Memperbarui file view `estate_booking_views.xml` untuk menyajikan informasi parameter termin dan sisa kewajiban pembayaran secara informatif.

**Non-Goals:**

- Menerbitkan dokumen draf faktur pelanggan (`account.move`) secara otomatis (dialokasikan ke change `integrate-customer-invoices`).
- Menampilkan tagihan cicilan pada portal pelanggan `/my/invoices` (dialokasikan ke change `ui-customer-portal-invoices`).
- Memodifikasi mekanisme webhook gateway pembayaran bawaan Odoo (sudah tuntas pada Fase 4).

## Decisions

### 1. Struktur Field Termin dan Sisa Kewajiban pada Model Reservasi

- **Rationale:** Pada model `estate.booking`, ditambahkan field `installment_term` bertipe Integer (default 12, required=True) untuk menentukan kuantitas termin pembayaran bulanan, serta field `remaining_amount` bertipe Monetary (computed) yang menghitung sisa kewajiban finansial dari `property_id.selling_price or property_id.expected_price - booking_fee_paid`. Pendekatan ini memberikan kejelasan kalkulasi finansial antara harga properti, uang tanda jadi yang telah disetorkan, dan sisa pokok piutang.
- **Alternatives Considered:** Menggunakan tipe data Selection statis (misal 12, 24, 36 bulan); ditolak karena tipe Integer memberikan fleksibilitas penuh bagi staf operasional jika terdapat kesepakatan skema termin kustom (misal 6, 18, atau 48 bulan).

### 2. Logika Distribusi Angsuran dan Penanganan Pembulatan Mata Uang

- **Rationale:** Nilai sisa kewajiban dibagi dengan jumlah termin (`remaining_amount / installment_term`). Setiap baris angsuran dibulatkan sesuai presisi desimal mata uang yang aktif (`currency_id.round`). Untuk mencegah disparitas selisih pembulatan sen antara total cicilan dan sisa kewajiban pokok, selisih desimal pembulatan diakumulasikan secara tepat pada baris termin terakhir (`remaining_amount - sum_previous_installments`). Tanggal jatuh tempo per termin dihitung bertahap per bulan: `booking_date + relativedelta(months=i)` mulai dari bulan ke-1 hingga bulan ke-N.
- **Alternatives Considered:** Mengabaikan pembulatan mata uang dan membiarkan pecahan mengambang (*float precision*); ditolak karena berisiko memicu ketidakseimbangan jurnal (*unbalanced journal entries*) saat draf faktur dibuat pada modul akuntansi.

### 3. Pemicuan Otomatis Idempoten pada Siklus action_confirm

- **Rationale:** Method `action_confirm()` pada `estate.booking` diperluas untuk memanggil `_generate_installments()` secara otomatis sesaat setelah status reservasi ditetapkan menjadi `confirmed`. Logika pembuatan jadwal memeriksa keberadaan cicilan yang sudah ada (`if not record.installment_ids`). Jika jadwal sudah terbentuk, sistem mempertahankan data yang ada tanpa melakukan duplikasi, sehingga aman dari pemicuan webhook ganda.
- **Alternatives Considered:** Menjalankan pembuatan cicilan melalui scheduled action (cron); ditolak karena agen properti dan klien mengharapkan transparansi jadwal cicilan seketika setelah pembayaran uang muka terverifikasi lunas.

### 4. Proteksi Keamanan Regenerasi Manual oleh Agen Properti

- **Rationale:** Tombol aksi manual "Buat Jadwal Cicilan" disediakan pada header form view `estate.booking`. Sebelum menghapus atau memperbarui baris cicilan yang belum lunas, sistem memeriksa apakah terdapat rekaman `estate.installment` yang telah memiliki `invoice_id` (telah berfaktur). Jika ditemukan, sistem membatalkan aksi dan melempar `UserError`. Jika belum ada faktur yang terbentuk, sistem mengizinkan pembaruan jadwal cicilan sesuai parameter termin terkini.
- **Alternatives Considered:** Menghapus paksa seluruh cicilan termasuk yang telah memiliki relasi faktur; ditolak keras karena akan merusak integritas referensial dan jejak audit pada modul akuntansi.

## Risks / Trade-offs

- [Risk] Nilai sisa kewajiban (`remaining_amount`) bernilai nol atau negatif jika nilai uang tanda jadi sama dengan atau melebihi harga properti. → [Mitigation] Tambahkan validasi (*constrains*) pada `estate.booking` bahwa `booking_fee_paid` tidak boleh melebihi harga properti, dan pembuatan jadwal cicilan hanya dieksekusi jika `remaining_amount > 0`.
- [Risk] Pergeseran kalender pada tanggal jatuh tempo akhir bulan (misalnya tanggal 31 Januari ke bulan Februari). → [Mitigation] Pustaka `relativedelta(months=i)` secara otomatis menangani normalisasi kalender akhir bulan secara aman dan presisi sesuai standar Odoo.
