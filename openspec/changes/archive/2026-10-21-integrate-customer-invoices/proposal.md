## Why

Entitas jadwal cicilan pembiayaan (`estate.installment`) telah berhasil dibentuk secara otomatis pasca-konfirmasi reservasi, namun sistem belum terintegrasi dengan modul akuntansi resmi Odoo 17 (`account`). Ketiadaan integrasi ini menyebabkan jadwal cicilan hanya tercatat sebagai data administratif lokal tanpa memiliki dokumen finansial sah berupa faktur pelanggan (*Customer Invoice* / `account.move`). Staf keuangan tidak dapat membukukan piutang, mencatat pembayaran termin, atau melakukan rekonsiliasi kas secara sistematis. Integrasi penerbitan draf faktur pelanggan bagi setiap cicilan yang jatuh tempo sangat dibutuhkan untuk mengotomatisasi siklus penagihan dan menjadi prasyarat agar tagihan dapat dipublikasikan ke portal pelanggan.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Capability `installment-invoicing`, Change `integrate-customer-invoices`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 1.2 (Tujuan Bisnis), Bagian 3.1 (Ketergantungan Modul), & Bagian 3.2 (Model Data).

## What Changes

- Mengimplementasikan method pembuatan faktur pelanggan `action_create_invoice()` pada model `estate.installment` yang menerbitkan dokumen `account.move` bertipe `out_invoice` dengan rincian partner pembeli, referensi pemesanan, baris faktur produk/keterangan cicilan, nilai nominal, dan tanggal jatuh tempo yang valid.
- Menambahkan method navigasi pintar `action_view_invoice()` dan sinkronisasi status pembayaran cicilan (`state`) secara dinamis berdasarkan status pelunasan faktur akuntansi (`payment_state` pada `account.move`).
- Mengimplementasikan scheduled action (cron job) `_cron_generate_due_installment_invoices()` pada `estate.installment` untuk memindai dan menerbitkan draf faktur secara otomatis bagi seluruh cicilan yang telah mencapai atau melewati tanggal jatuh tempo (`due_date <= context_today`).
- Mendaftarkan file data `addons/estate_booking/data/estate_installment_cron.xml` pada `__manifest__.py` untuk aktivasi cron job harian.
- Memperbarui antarmuka `addons/estate_booking/views/estate_installment_views.xml` dengan menambahkan header form, statusbar, tombol aksi "Terbitkan Faktur", dan tautan pintas stat button menuju faktur terkait.

## Capabilities

### New Capabilities

Tidak ada.

### Modified Capabilities

- `installment-invoicing`: Menambahkan kemampuan integrasi penerbitan draf faktur pelanggan (`account.move`) untuk jadwal cicilan `estate.installment`, sinkronisasi status pelunasan dengan akuntansi, dan eksekusi penerbitan faktur berkala terjadwal (cron job) untuk cicilan yang jatuh tempo.

## Impact

- **Files created:**
  - `addons/estate_booking/data/estate_installment_cron.xml`
  - `openspec/changes/integrate-customer-invoices/specs/installment-invoicing/spec.md`
- **Files modified:**
  - `addons/estate_booking/__manifest__.py`
  - `addons/estate_booking/models/estate_installment.py`
  - `addons/estate_booking/views/estate_installment_views.xml`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 3 hours.
