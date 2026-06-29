# Integration Testing - Evalio

## Tujuan

Integration testing memastikan komponen frontend, REST API FastAPI, service sistem pakar, forward chaining engine, dan JSON knowledge base bekerja sebagai satu alur yang konsisten tanpa mengubah implementasi aplikasi.

## Strategi Integrasi

Strategi yang digunakan adalah Sandwich Integration.

Alasan pemilihan:

- Lapisan bawah seperti JSON knowledge base, validator, loader, dan forward chaining dapat diuji lebih awal sebagai domain logic.
- Lapisan atas seperti endpoint REST API dapat diuji dengan driver HTTP melalui FastAPI TestClient.
- Frontend tetap diuji melalui skenario UAT/manual tanpa mengubah UI atau business logic.

## Pemetaan Komponen

| Lapisan | Komponen | Teknik Uji | Stub/Driver |
|---|---|---|---|
| Data | JSON knowledge repository | Validasi pemuatan knowledge dan referensi rule | Tidak diperlukan stub karena repository asli digunakan |
| Domain | ForwardChainingEngine, ExpertSystemService | Pytest unit/regression | Test driver memanggil service langsung |
| API | FastAPI router `/evaluation`, `/health`, `/version` | Pytest + FastAPI TestClient | HTTP driver internal TestClient |
| Frontend | HTML/CSS/JavaScript | UAT manual berbasis browser | Backend API asli pada `http://127.0.0.1:8000` |
| Non-fungsional | Endpoint `/evaluation` | k6 load test dan stress test | k6 sebagai traffic driver |

## Skenario Integration Test

| ID | Alur Integrasi | Input | Expected Result |
|---|---|---|---|
| INT-API-01 | Client memanggil `GET /health` | Tidak ada payload | API mengembalikan status layanan `ok` |
| INT-API-02 | Client memanggil `GET /version` | Tidak ada payload | API mengembalikan versi API dan knowledge |
| INT-API-03 | Client mengirim fakta lengkap ke `POST /evaluation` | Seluruh fakta pembentuk RC01-RC08 | Response sukses, keputusan READY, risiko LOW |
| INT-API-04 | Client mengirim fakta pembentuk tujuh kriteria | Fakta RC01-RC07 | Response sukses, keputusan IMPROVEMENT |
| INT-API-05 | Client mengirim fakta kosong | `facts: []` | Response sukses, keputusan NOT_READY, risiko HIGH |
| INT-API-06 | Client mengirim format fakta tidak valid | `facts: ["INVALID_FACT"]` | Response validasi 422 |

## Perintah Eksekusi

```bash
python -m pip install -r requirements-test.txt
pytest -m api
pytest -m unit
pytest
```

## Kriteria Lulus

- Semua integration test berstatus Pass.
- Tidak ada perubahan pada source code aplikasi.
- Coverage minimal 75% sesuai konfigurasi `pytest.ini`.
- Laporan HTML coverage tersedia di `reports/coverage_html`.
