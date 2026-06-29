# Laporan Pengujian dan Rekomendasi Kualitas Perangkat Lunak

## Halaman Judul

- Nama proyek: Evalio - Event Readiness Expert System
- Mata kuliah: Pengujian dan Penjaminan Kualitas Perangkat Lunak
- Kode mata kuliah: 22A0113153
- Semester: Genap 2025/2026
- Anggota kelompok: Isi nama dan NIM anggota kelompok
- Program studi/jurusan/kampus: Isi sesuai data kelompok
- Repository GitHub: Isi tautan repository

## BAB I - Pendahuluan

### 1.1 Latar Belakang Aplikasi

Evalio adalah sistem pakar untuk menentukan tingkat kesiapan penyelenggaraan event berdasarkan faktor risiko. Aplikasi menggunakan REST API FastAPI, frontend HTML/CSS/JavaScript, metode Forward Chaining, dan JSON Knowledge Base sebagai basis pengetahuan.

Output utama aplikasi adalah keputusan kesiapan event:

- READY: event siap dilaksanakan.
- IMPROVEMENT: event dapat dilaksanakan setelah beberapa aspek diperbaiki.
- NOT_READY: event belum layak dilaksanakan.

### 1.2 Ruang Lingkup Pengujian

Modul yang diuji:

- Frontend halaman awal, halaman evaluasi, dan halaman hasil.
- Endpoint REST API `/`, `/version`, `/health`, dan `/evaluation`.
- Alur Forward Chaining dari fakta ke kriteria dan keputusan.
- JSON Knowledge Base sebagai sumber fakta, kriteria, aturan, keputusan, dan rekomendasi.
- Non-functional testing berupa performance, security review, dan usability.

Di luar ruang lingkup:

- Perubahan source code backend.
- Perubahan source code frontend.
- Perubahan business logic, struktur JSON, endpoint, UI, atau arsitektur.
- Penambahan fitur baru.

### 1.3 Lingkungan Pengujian

| Komponen | Spesifikasi |
|---|---|
| Backend | FastAPI, Python 3.13 |
| Frontend | HTML, CSS, JavaScript |
| Test automation | pytest, pytest-cov, httpx/FastAPI TestClient |
| Performance | k6 |
| CI/CD | GitHub Actions |
| OS pengujian | Isi OS penguji |
| Browser | Isi browser penguji |
| Base URL backend | `http://127.0.0.1:8000` |

## BAB II - Rencana dan Skenario Pengujian Integrasi & UAT

### 2.1 Strategi Integration Testing

Strategi yang digunakan adalah Sandwich Integration. Pengujian dilakukan dari lapisan domain dan data melalui pytest unit/regression, lalu dari lapisan API melalui FastAPI TestClient, dan dilengkapi UAT manual pada frontend.

Driver yang digunakan:

- Pytest driver untuk memanggil `ExpertSystemService`.
- FastAPI TestClient sebagai driver HTTP internal.
- k6 sebagai traffic driver untuk pengujian beban.

Stub tidak digunakan karena seluruh komponen aplikasi sudah tersedia dan dianggap production ready.

### 2.2 Tabel Skenario UAT

Skenario UAT lengkap tersedia pada `docs/testing/uat_scenarios.md`.

## BAB III - Execution, Automation, & Regression Testing

### 3.1 Log Laporan Cacat

Template bug report tersedia pada `docs/testing/bug_report_template.md`. Jika tidak ditemukan bug saat eksekusi, bagian ini diisi dengan keterangan "Tidak ditemukan defect fungsional pada periode pengujian".

### 3.2 Implementasi Automation & Regression Test

Test suite dibuat pada folder `tests/`:

- `tests/api/test_system_api.py`: validasi endpoint sistem.
- `tests/api/test_evaluation_api.py`: validasi endpoint evaluasi READY, IMPROVEMENT, NOT_READY, dan skenario invalid.
- `tests/unit/test_expert_system_regression.py`: validasi regresi Forward Chaining dan rekomendasi.

Perintah eksekusi:

```bash
python -m pip install -r requirements-test.txt
pytest
```

### 3.3 Code Coverage

Coverage dikonfigurasi melalui `pytest.ini` dan `.coveragerc` dengan target minimal 75%.

Output yang dihasilkan:

- Terminal coverage summary.
- HTML coverage report: `reports/coverage_html`.
- XML coverage report: `reports/coverage.xml`.

Hasil verifikasi otomatis pada 29 Juni 2026 menunjukkan 11 test lulus dan total coverage 80,75%, sehingga target minimal 75% terpenuhi.

### 3.4 Integrasi CI/CD

Workflow GitHub Actions tersedia di `.github/workflows/test.yml`. Pipeline berjalan pada push ke `main`/`master` dan pull request, memasang dependency, menjalankan pytest, serta mengunggah HTML coverage sebagai artifact.

## BAB IV - Non-Functional Testing Execution

### 4.1 Performance Testing dengan k6

Skrip k6:

- Load test: `performance/evaluation-load-test.js`, 50 VU selama 1 menit.
- Stress test: `performance/evaluation-stress-test.js`, ramp-up bertahap sampai 200 VU.

Perintah:

```bash
k6 run performance/evaluation-load-test.js
k6 run performance/evaluation-stress-test.js
```

Metrik yang dicatat:

- Response Time P95.
- Error Rate.
- Throughput.

### 4.2 Security Testing

Security testing dilakukan melalui static security review, dependency audit Python, dan checklist OWASP API. Dokumen lengkap tersedia pada `docs/testing/security_testing.md`.

Perintah audit:

```bash
pip-audit -r backend/requirements.txt
```

Hasil audit dependency pada 29 Juni 2026: `No known vulnerabilities found`.

### 4.3 Usability Testing Sederhana

Kuesioner SUS tersedia pada `docs/testing/sus_questionnaire.md`. Minimal tiga responden diminta menjalankan aplikasi lalu mengisi 10 pernyataan SUS. Skor dihitung menggunakan rumus standar SUS.

## BAB V - Metrik Kualitas dan Rekomendasi Perbaikan

### 5.1 Perhitungan Quality Metrics

Template perhitungan Passed Rate dan Defect Density tersedia pada `docs/testing/quality_metrics_template.md`.

### 5.2 Analisis Defect Life Cycle

Setiap defect dicatat menggunakan status:

Open, Assigned, In Progress, Fixed, Retest, Closed, Reopened, atau Deferred.

Area yang perlu diamati sebagai error-prone modules:

- Mapping fakta ke kriteria.
- Rule global penentuan keputusan.
- Validasi payload `/evaluation`.
- Penyimpanan hasil evaluasi di browser localStorage.
- Ketahanan endpoint `/evaluation` saat load tinggi.

### 5.3 Rekomendasi Solutif

Rekomendasi lengkap tersedia pada `reports/recommendation_report.md`. Semua rekomendasi bersifat SQA/operasional dan tidak mengubah implementasi aplikasi saat ini.

## Kesimpulan

Paket pengujian ini menyediakan dokumen UAT, integration testing, bug report, automation test, API test, coverage, CI/CD, k6 performance test, security review, SUS, quality metrics, dan rekomendasi kualitas untuk Evalio tanpa mengubah perilaku aplikasi.
