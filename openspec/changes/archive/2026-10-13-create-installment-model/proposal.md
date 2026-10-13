## Why

Sistem telah memiliki model `estate.booking` yang memiliki relasi `installment_ids` ke `estate.installment`, namun model `estate.installment` belum didefinisikan pada modul `estate_booking`. Ketiadaan model ini menghambat pencatatan jadwal tagihan pembiayaan bertahap serta menyebabkan registry ORM Odoo tidak dapat meresolusi relasi `installment_ids`. Pembuatan model `estate.installment` diperlukan sebagai landasan pencatatan tagihan bulanan, pelacakan tanggal jatuh tempo, dan integrasi penagihan otomatis dengan modul akuntansi pada change selanjutnya.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 2, capability `property-booking-models`, change `create-installment-model`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 3.2.

## What Changes

- Menambahkan model Odoo baru `estate.installment` pada paket `addons/estate_booking/models` untuk mencatat jadwal cicilan pelanggan per bulan.
- Menyediakan field relasi reservasi (`booking_id`), nama/keterangan (`name`), tanggal jatuh tempo (`due_date`), nilai tagihan (`amount`), mata uang teknis (`currency_id`), relasi faktur akuntansi (`invoice_id`), serta status cicilan (`state`).
- Mendefinisikan pilihan status cicilan `unpaid`, `paid`, dan `late` dengan nilai awal `unpaid`.
- Mendaftarkan model baru pada `addons/estate_booking/models/__init__.py`.

## Capabilities

### New Capabilities

Tidak ada.

### Modified Capabilities

- `property-booking-models`: Menambahkan kemampuan untuk mencatat jadwal cicilan pembiayaan (`estate.installment`) yang terhubung dengan dokumen reservasi, mencatat jatuh tempo dan nominal tagihan, serta melacak status pembayaran cicilan.

## Impact

- **Files created:**
  - `addons/estate_booking/models/estate_installment.py`
- **Files modified:**
  - `addons/estate_booking/models/__init__.py`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 4 hours.
