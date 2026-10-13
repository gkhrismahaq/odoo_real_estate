## Why

Calon pembeli dan pengunjung situs memerlukan halaman web publik yang dapat diakses secara terbuka tanpa perlu login ke antarmuka internal Odoo untuk menelusuri katalog unit properti yang tersedia (berstatus baru/tersedia), lengkap dengan nama, tipe properti, harga bukaan, kode pos, dan spesifikasi dasarnya.
> **Reference:** [TSD](../../docs/01-estate_booking/tsd.md) — Bagian 1.3 & 2.2.

## What Changes

- Pembuatan paket direktori `addons/estate_booking/controllers` beserta inisialisasi controller Odoo.
- Implementasi controller `PropertyCatalogController` dengan route `/properties` bertipe HTTP, otentikasi publik (`auth='public'`), dan dukungan layout website Odoo (`website=True`).
- Controller mengambil daftar rekaman `estate.property` yang berstatus `new` dan masih aktif secara aman untuk disajikan ke pengunjung publik.
- Pembuatan berkas template QWeb `addons/estate_booking/views/portal_property_catalog_templates.xml` yang mewarisi `website.layout` untuk menyajikan kartu grid katalog properti yang responsif, rapi, dan informatif.
- Pendaftaran controller pada `addons/estate_booking/__init__.py`.
- Pendaftaran berkas XML template QWeb pada deklarasi `data` di `addons/estate_booking/__manifest__.py`.

## Capabilities

### New Capabilities
- `portal-property-catalog`: Menyediakan antarmuka publik web portal bagi pengunjung dan calon klien untuk menelusuri katalog properti yang tersedia untuk dipesan.

## Impact

- **Files created:**
  - `addons/estate_booking/controllers/__init__.py`
  - `addons/estate_booking/controllers/main.py`
  - `addons/estate_booking/views/portal_property_catalog_templates.xml`
- **Files modified:**
  - `addons/estate_booking/__init__.py`
  - `addons/estate_booking/__manifest__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/tsd.md` (Bagian 1.3, 2.1, 2.2, 3.4)
  - `docs/01-estate_booking/roadmap.md` (Fase 3, Bagian 3.1)

**Estimated effort:** 3 hours.
