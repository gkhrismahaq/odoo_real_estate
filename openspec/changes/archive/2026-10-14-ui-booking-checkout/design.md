## Context

Pada tahap sebelumnya, antarmuka publik katalog (`/properties`) dan rincian properti (`/property/<id>`) telah selesai dibangun, di mana tombol "Book Now" mengarah ke `/booking/checkout?property_id=<id>`. Sesuai SSOT TSD Bagian 2.2 & 3.2, sistem memerlukan alur formulir checkout yang mengonversi minat pembeli menjadi dokumen draf reservasi `estate.booking` sebelum diteruskan ke gerbang pembayaran pada Fase 4.
Lihat `proposal.md` untuk rincian latar belakang bisnis.

## Goals / Non-Goals

**Goals:**
- Menyediakan rute GET `/booking/checkout` pada controller untuk menyajikan formulir identitas pembeli dan ringkasan unit properti yang valid (`status == 'new'` dan `active == True`).
- Menyediakan rute POST `/booking/checkout/submit` untuk memvalidasi input, membuat/mengaitkan kontak `res.partner`, dan menerbitkan dokumen draf `estate.booking`.
- Mengimplementasikan pola Post-Redirect-Get menuju rute GET `/booking/confirmation/<int:booking_id>` guna menyajikan nomor referensi booking dan instruksi pelunasan tanda jadi.
- Membuat template QWeb `addons/estate_booking/views/portal_booking_checkout_templates.xml` dengan tata letak modern 2-kolom yang konsisten dan minimalis.
- Menghubungkan nilai `booking_fee_paid` pada dokumen booking dengan nilai `booking_fee` dari unit properti terkait.
- Mendaftarkan berkas view baru pada elemen `data` di `addons/estate_booking/__manifest__.py`.

**Non-Goals:**
- Integrasi tombol pembayaran dengan payment provider / test provider Odoo (fokus pada Fase 4: `integrate-payment-transaction`).
- Pembuatan jadwal termin tagihan cicilan `estate.installment` (dikelola pada Fase 5).

## Decisions

### 1. Pola Pengelolaan Partner dan Pembuatan Reservasi via `sudo()`
- **Rationale:** Pengunjung situs mengakses formulir secara publik (`auth='public'`). Untuk mencegah kendala hak akses saat membuat atau mencari data pemesan (`res.partner`) serta dokumen `estate.booking`, controller mengeksekusi operasi ORM menggunakan hak akses terkontrol `.sudo()`. Dokumen booking diinisialisasi dalam status `draft` dengan nomor referensi unik terstruktur (misal: `BOOK-{property_id}-{timestamp}`).
- **Alternatives Considered:** Memaksa pengunjung mendaftar akun portal dan login terlebih dahulu sebelum mengisi formulir (meningkatkan friksi dan menurunkan tingkat konversi pemesanan).

### 2. Tata Letak 2-Kolom Minimalis (Formulir Pemesan & Ringkasan Unit)
- **Rationale:** Menempatkan formulir isian identitas di kolom utama (`col-lg-7`) dan kartu ringkasan unit properti beserta nilai uang tanda jadi di kolom samping (`col-lg-5`) memberikan visibilitas penuh bagi pembeli terhadap unit yang sedang dipesan saat melengkapi data.
- **Alternatives Considered:** Tata letak satu kolom bertumpuk (ringkasan unit tersembunyi di atas atau di bawah formulir).

### 3. Arsitektur Post-Redirect-Get (PRG) Menuju Halaman Konfirmasi
- **Rationale:** Setelah form berhasil divalidasi dan dokumen booking diterbitkan, controller melakukan pengalihan HTTP redirect ke `/booking/confirmation/<booking_id>`. Hal ini mencegah duplikasi pembuatan booking jika pembeli me-refresh peramban serta menyediakan antarmuka mandiri untuk mengaitkan widget pembayaran pada fase berikutnya.
- **Alternatives Considered:** Menampilkan pesan sukses langsung pada respons POST tanpa pengalihan (rentan duplikasi data saat reload halaman).

## Risks / Trade-offs

- [Risk: Calon pembeli memasukkan alamat email yang tidak valid atau formulir dikirim kosong] → Controller melakukan validasi ketat pada server-side terhadap field wajib (nama, email, telepon), dan mengembalikan formulir dengan pesan peringatan jika validasi gagal.
- [Risk: Unit properti diambil atau statusnya berubah saat pembeli sedang mengisi formulir checkout] → Controller memverifikasi ulang bahwa `property.status == 'new'` sebelum membuat dokumen booking. Jika unit sudah tidak tersedia, pengunjung diarahkan kembali ke katalog `/properties` dengan pesan informasi.
