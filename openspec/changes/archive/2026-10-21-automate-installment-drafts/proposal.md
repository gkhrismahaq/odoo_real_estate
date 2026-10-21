## Why

Saat ini, dokumen pemesanan (`estate.booking`) yang berhasil terkonfirmasi pasca-pembayaran uang tanda jadi belum menghasilkan jadwal penagihan cicilan secara otomatis. Pengguna internal atau agen properti harus menginput baris demi baris entitas jadwal pembiayaan (`estate.installment`) secara manual, yang rentan terhadap kekeliruan perhitungan nominal termin, ketidaktepatan tanggal jatuh tempo bulanan, dan kelalaian operasional. Otomatisasi pembentukan draf jadwal cicilan (*installment drafts*) sesaat setelah pembayaran tanda jadi lunas sangat esensial untuk menjamin kesinambungan alur penagihan piutang pelanggan dan menjadi prasyarat sebelum penerbitan faktur berkala pada modul akuntansi.
> **Reference:** [Roadmap](../../../docs/01-estate_booking/roadmap.md) — Fase 5, Capability `installment-invoicing`, Change `automate-installment-drafts`.
> **Reference:** [TSD](../../../docs/01-estate_booking/tsd.md) — Bagian 2.2 (Alur Proses Bisnis butir 4) & Bagian 3.2 (Model Data `estate.booking` dan `estate.installment`).

## What Changes

- Menambahkan field konfigurasi termin cicilan `installment_term` (Integer, default 12) serta field perhitungan nilai sisa tagihan properti `remaining_amount` (Monetary) pada model `estate.booking`.
- Mengimplementasikan logika kalkulasi dan pembuatan otomatis baris jadwal cicilan `estate.installment` melalui method `action_generate_installments()` pada model `estate.booking` dengan pembagian nominal merata dan tanggal jatuh tempo bulanan bertahap secara idempoten.
- Mengintegrasikan pemanggilan pembuatan draf jadwal cicilan secara otomatis ke dalam siklus konfirmasi dokumen reservasi (`action_confirm()`) pada `estate.booking` sesaat setelah status reservasi beralih menjadi `confirmed`.
- Menambahkan tombol aksi manual "Buat Jadwal Cicilan" dan field termin/sisa pembayaran pada tampilan backend form `estate.booking` (`estate_booking_views.xml`) agar agen properti dapat meninjau serta menyesuaikan parameter termin sebelum tagihan diterbitkan.

## Capabilities

### New Capabilities

- `installment-invoicing`: Otomatisasi pembuatan deretan draf jadwal cicilan pembiayaan properti (`estate.installment`) berdasarkan jumlah termin dan nilai sisa pembayaran setelah pembayaran uang muka (*booking fee*) terkonfirmasi lunas.

### Modified Capabilities

Tidak ada.

## Impact

- **Files created:**
  - `openspec/changes/automate-installment-drafts/specs/installment-invoicing/spec.md` (delta spec untuk new capability)
- **Files modified:**
  - `addons/estate_booking/models/estate_booking.py`
  - `addons/estate_booking/views/estate_booking_views.xml`
- **SSOT documents referenced:**
  - `docs/01-estate_booking/roadmap.md`
  - `docs/01-estate_booking/tsd.md`

**Estimated effort:** 3 hours.
