## Context

Model data `estate.booking` dan `estate.installment` telah diimplementasikan beserta konfigurasi hak aksesnya (ACL dan Record Rules). Agar pengguna internal (agen properti) dapat berinteraksi secara visual, dibutuhkan tampilan backend Odoo 17 yang meliputi Tree (List) view, Form view, Search filter, serta integrasi struktur menu navigasi yang terhubung dengan modul dasar `estate`.
Lihat `proposal.md` untuk motivasi dan latar belakang kebutuhan bisnis.

## Goals / Non-Goals

**Goals:**
- Menyediakan Tree/List view dan Form view yang rapi, komprehensif, dan terstandarisasi untuk model `estate.booking`.
- Menyediakan Tree/List view dan Form view untuk model `estate.installment`.
- Menyediakan Search filter view untuk pencarian, pemfilteran berdasarkan status, dan pengelompokan (group by) pada kedua model.
- Mengimplementasikan form header pada formulir reservasi dengan widget statusbar dan tombol transisi status (`action_waiting_payment`, `action_confirm`, `action_cancel`).
- Menyediakan tab inline notebook pada formulir reservasi untuk menampilkan daftar jadwal cicilan (`installment_ids`).
- Membentuk struktur navigasi menu terintegrasi di bawah root menu `estate.estate_property_root` ("Manajemen Properti").
- Mendaftarkan seluruh file XML pada deklarasi `data` di `addons/estate_booking/__manifest__.py` dengan urutan dependensi yang benar.

**Non-Goals:**
- Pembuatan antarmuka publik portal website (dikelola pada Fase 3).
- Otomatisasi generate baris cicilan atau penerbitan faktur akuntansi (dikelola pada Fase 5).
- Memodifikasi atau menghapus view bawaan pada modul `estate`.

## Decisions

### 1. Pemisahan Modular Berkas XML (Views dan Menus)
- **Rationale:** Memisahkan definisi action/view per model (`estate_booking_views.xml`, `estate_installment_views.xml`) dan berkas menu navigasi terpisah (`estate_booking_menus.xml`) menjaga prinsip *separation of concerns*, mencegah duplikasi, dan mengeliminasi risiko parsing error terkait referensi ID action yang belum terdefinisi.
- **Alternatives Considered:** Menggabungkan seluruh view dan menu ke dalam satu file XML tunggal (membuat kode panjang, sulit dibaca, dan rentan salah urutan deklarasi ID).

### 2. Integrasi Navigasi Menu di Bawah Root Menu Properti
- **Rationale:** Mengaitkan menu baru di bawah root menu yang sudah ada, yaitu `estate.estate_property_root` ("Manajemen Properti"), menghasilkan pengalaman terpadu bagi agen properti. Dibuat menu grup level-1 baru bernama "Reservasi" (`estate_booking_menu_root`) yang menaungi submenu "Daftar Reservasi" dan "Jadwal Cicilan".
- **Alternatives Considered:** Membuat top-level application menu baru tersendiri di app switcher (menghasilkan fragmentasi menu untuk modul properti yang sebenarnya saling terkait).

### 3. Pengendalian Status Dokumen Melalui Form Header & Statusbar
- **Rationale:** Mengikuti standar UX Odoo 17, form reservasi dilengkapi elemen `<header>` yang menampung tombol aksi status dengan atribut `invisible` kondisional:
  - Tombol "Menunggu Pembayaran" (`action_waiting_payment`): hanya muncul saat `state == 'draft'`.
  - Tombol "Konfirmasi" (`action_confirm`, class `btn-primary`): hanya muncul saat `state == 'waiting_payment'`.
  - Tombol "Batalkan" (`action_cancel`): hanya muncul saat `state == 'confirmed'`.
  - Statusbar interaktif: `<field name="state" widget="statusbar" statusbar_visible="draft,waiting_payment,confirmed" />`.
- **Alternatives Considered:** Mengubah status manual langsung dari field selection biasa tanpa kontrol tombol action (rentan inkonsistensi data karena membypass validasi method Python).

### 4. Tab Notebook Inline untuk Relasi Jadwal Cicilan
- **Rationale:** Menampilkan relasi `installment_ids` di dalam notebook tab pada form reservasi memungkinkan agen langsung meninjau seluruh termin cicilan beserta statusnya secara kontekstual tanpa membuka menu cicilan secara terpisah.
- **Alternatives Considered:** Mengharuskan pengguna membuka menu cicilan secara manual dan memfilter berdasarkan nomor reservasi (aliran kerja lambat dan tidak ergonomis).

## Risks / Trade-offs

- [Risk: Kesalahan urutan pemuatan berkas XML di manifest] → Pastikan pada `__manifest__.py` file view action (`views/estate_booking_views.xml` dan `views/estate_installment_views.xml`) dideklarasikan SEBELUM file menu (`views/estate_booking_menus.xml`).
- [Risk: Inkonsistensi atribut invisible/readonly Odoo 17] → Gunakan sintaks domain ekspresi Odoo 17 (seperti `invisible="state != 'draft'"` atau python domain ekspresi yang didukung Odoo 17) guna menjamin kompatibilitas penuh.
