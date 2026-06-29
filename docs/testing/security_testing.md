# Security Testing - Evalio

## Ruang Lingkup

Security testing dilakukan sebagai review statis dan audit dependency untuk proyek FastAPI. Karena aplikasi dinyatakan production ready, dokumen ini tidak menginstruksikan perubahan business logic, endpoint, JSON knowledge base, atau UI.

## Pendekatan

- Static security review terhadap struktur endpoint, validasi request Pydantic, CORS, dan penanganan exception.
- Dependency audit menggunakan `pip-audit`.
- OWASP API Security checklist untuk endpoint REST.
- Verifikasi bahwa input invalid ditolak oleh skema API.

## Perintah Audit Dependency

```bash
python -m pip install -r requirements-test.txt
pip-audit -r backend/requirements.txt
```

## Checklist OWASP API

| Area | Observasi | Status | Bukti |
|---|---|---|---|
| API1 Broken Object Level Authorization | Tidak ada resource per pengguna pada scope aplikasi ini. | Review | Endpoint publik terbatas pada evaluasi dan informasi sistem |
| API2 Broken Authentication | Tidak ada modul autentikasi pada scope aplikasi. | N/A | Aplikasi evaluasi publik |
| API3 Broken Object Property Level Authorization | Response mengikuti model Pydantic dan tidak membuka data rahasia. | Review | `EvaluationResponse` |
| API4 Unrestricted Resource Consumption | Perlu diuji dengan k6 untuk batas latensi dan error rate. | Pending | `performance/evaluation-load-test.js` |
| API5 Broken Function Level Authorization | Endpoint yang tersedia tidak memuat fungsi administratif. | Review | Router FastAPI |
| API6 Unrestricted Access to Sensitive Business Flows | Evaluasi dapat dipanggil publik; mitigasi operasional dapat berupa rate limiting pada deployment. | Recommendation | Tidak mengubah source code |
| API7 Server Side Request Forgery | Tidak ada input URL eksternal yang diproses backend. | Pass | Payload hanya berisi daftar fakta |
| API8 Security Misconfiguration | CORS dibatasi pada localhost port pengembangan. Perlu validasi konfigurasi produksi sebelum deploy. | Review | Middleware CORS |
| API9 Improper Inventory Management | Endpoint dasar terdokumentasi dalam laporan pengujian. | Pass | `docs/testing/integration_testing.md` |
| API10 Unsafe Consumption of APIs | Backend tidak mengonsumsi API eksternal pada flow evaluasi. | Pass | Review source |

## Praktik Keamanan yang Direkomendasikan Tanpa Mengubah Implementasi

| Rekomendasi | Tujuan | Prioritas |
|---|---|---|
| Terapkan rate limiting pada reverse proxy atau API gateway produksi | Mengurangi risiko request berlebih pada `/evaluation` | High |
| Tambahkan security headers pada layer deployment | Memperkuat proteksi browser tanpa mengubah UI | Medium |
| Jalankan dependency audit pada CI | Mendeteksi library rentan sebelum rilis | High |
| Batasi CORS ke domain produksi resmi | Mengurangi akses lintas origin yang tidak diharapkan | High |
| Simpan bukti audit sebelum dan sesudah dependency update | Memenuhi kebutuhan dokumentasi tugas SQA | Medium |

## Catatan Adaptasi dari Panduan

Panduan kuliah memberi contoh Node.js/Express seperti Helmet.js, express-rate-limit, dan express-validator. Proyek ini menggunakan FastAPI, sehingga padanan pengujiannya adalah security headers/rate limiting pada deployment, validasi Pydantic, dan audit dependency Python.
