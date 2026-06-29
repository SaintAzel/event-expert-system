# Ringkasan Eksekusi Pengujian - Evalio

## Status Verifikasi Otomasi

Tanggal eksekusi: 29 Juni 2026

| Aktivitas | Hasil |
|---|---|
| Pytest API dan regression test | 11 passed |
| Coverage total | 80,75% |
| Target coverage | 75% |
| Status threshold coverage | Terpenuhi |
| Dependency audit | No known vulnerabilities found |

## Detail Pytest

Test suite yang dieksekusi:

- `tests/api/test_evaluation_api.py`: 5 passed
- `tests/api/test_system_api.py`: 3 passed
- `tests/unit/test_expert_system_regression.py`: 3 passed

Catatan:

- Terdapat satu warning dari dependency FastAPI/Starlette TestClient terkait deprecation penggunaan `httpx`; warning ini berasal dari dependency eksternal dan tidak mengubah hasil test.
- Laporan coverage HTML dihasilkan pada `reports/coverage_html`.
- Laporan coverage XML dihasilkan pada `reports/coverage.xml`.

## Detail Security Audit

Perintah yang digunakan:

```bash
pip-audit --cache-dir /private/tmp/pip-audit-cache -r backend/requirements.txt
```

Hasil:

```text
No known vulnerabilities found
```

## Status Performance Test

Skrip k6 telah dibuat tetapi belum dieksekusi dalam sesi ini karena k6 perlu tersedia di mesin penguji.

Skrip:

- `performance/evaluation-load-test.js`
- `performance/evaluation-stress-test.js`

Perintah eksekusi:

```bash
k6 run performance/evaluation-load-test.js
k6 run performance/evaluation-stress-test.js
```
