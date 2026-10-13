## Context

Modul `estate_booking` telah mendeklarasikan dependensi terhadap modul `website`. Untuk memenuhi kebutuhan bisnis Fase 3 (Antarmuka Publik) yang tertera pada roadmap dan TSD Bagian 1.3 & 2.2, sistem memerlukan endpoint web publik `/properties` dan template antarmuka QWeb untuk menampilkan daftar properti yang siap dipesan oleh calon pembeli.
Lihat `proposal.md` untuk motivasi bisnis dan ruang lingkup perubahan.

## Goals / Non-Goals

**Goals:**
- Menginisiasi paket direktori `addons/estate_booking/controllers` dan pendaftarannya pada `__init__.py`.
- Mengimplementasikan controller `PropertyCatalogController` dengan route publik `/properties` (`auth='public'`, `website=True`).
- Mengambil data properti aktif yang berstatus `new` dari model `estate.property` menggunakan hak baca terkontrol (`sudo()`).
- Membuat template QWeb di `addons/estate_booking/views/portal_property_catalog_templates.xml` berbasis `website.layout`.
- Merender kartu katalog responsif berbasis Bootstrap 5 Odoo 17 yang menampilkan nama, tipe, harga bukaan, kode pos, kamar tidur, luas bangunan, dan tautan menuju rute detail properti.
- Menyediakan penanganan kondisi tanpa data (*empty state*) yang informatif dan ramah pengunjung.
- Mendaftarkan berkas XML template QWeb pada deklarasi `data` di `addons/estate_booking/__manifest__.py`.

**Non-Goals:**
- Pembuatan rute dan template detail properti `/property/<id>` (dikelola pada change `ui-property-detail`).
- Pembuatan formulir checkout dan tombol pembayaran (dikelola pada change `ui-booking-checkout`).
- Modifikasi model backend `estate.property`.

## Decisions

### 1. Pembacaan Data Publik Terkontrol Melalui `sudo()` pada Controller
- **Rationale:** Pengguna anonim/publik (`base.group_public`) tidak memiliki hak baca langsung terhadap model backend `estate.property` melalui ACL untuk alasan keamanan. Menggunakan `request.env['estate.property'].sudo().search([('status', '=', 'new')])` di dalam method controller merupakan best practice Odoo untuk katalog website, di mana filter domain dikunci ketat di level backend dan hanya field non-sensitif yang diteruskan ke template QWeb.
- **Alternatives Considered:** Membuka izin baca model `estate.property` secara global untuk `base.group_public` di `ir.model.access.csv` (berisiko membuka data sensitif seperti margin harga, identitas pembeli, atau data internal).

### 2. Pemanfaatan Template Bawaan `website.layout`
- **Rationale:** Dengan mewarisi template bawaan `<t t-call="website.layout">`, halaman katalog secara otomatis mengadopsi navigasi navbar atas, footer, tema visual, serta aset JavaScript/CSS standar website Odoo 17 tanpa konfigurasi manual tambahan.
- **Alternatives Considered:** Membangun kerangka HTML lengkap secara mandiri (mengakibatkan hilangnya navigasi situs utama dan inkonsistensi tema portal).

### 3. Tata Letak Grid Responsif Menggunakan Bootstrap 5
- **Rationale:** Odoo 17 berjalan di atas Bootstrap 5. Memanfaatkan komponen grid `container py-5`, `row g-4`, dan kartu `col-12 col-md-6 col-lg-4` memastikan pengalaman visual optimal pada layar desktop, tablet, maupun ponsel tanpa ketergantungan CSS eksternal.
- **Alternatives Considered:** Menulis stylesheet CSS terpisah (memperbesar beban muat aset web dan rentan konflik dengan CSS website builder Odoo).

## Risks / Trade-offs

- [Risk: Eksposur properti yang sudah dipesan atau terjual ke publik] → Filter domain controller secara absolut mengunci kriteria hanya record yang berstatus `status == 'new'` dan berstatus aktif (`active == True`).
- [Risk: Controller gagal dikenali server Odoo] → Pastikan `controllers` diimpor di `addons/estate_booking/__init__.py` dan modul controller diimpor di `addons/estate_booking/controllers/__init__.py`.
