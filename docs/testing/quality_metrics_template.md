# Quality Metrics Template - Evalio

## Passed Rate

Rumus:

```text
Passed Rate = (Jumlah Test Case Pass / Total Test Case Dieksekusi) x 100%
```

Template:

| Jenis Pengujian | Total Test Case | Pass | Fail | Pending | Passed Rate |
|---|---:|---:|---:|---:|---:|
| UAT | 10 | 0 | 0 | 10 | 0% |
| Integration Test | 6 | 0 | 0 | 6 | 0% |
| API Automation | 8 | 8 | 0 | 0 | 100% |
| Performance Test | 2 | 0 | 0 | 2 | 0% |
| Security Review | 10 | 0 | 0 | 10 | 0% |

## Defect Density

Rumus:

```text
Defect Density = Jumlah Defect / Jumlah Modul yang Diuji
```

Template:

| Modul | Jumlah Defect | Ukuran Modul | Defect Density | Catatan |
|---|---:|---:|---:|---|
| Frontend Evaluasi | 0 | 1 | 0 | Diisi setelah UAT |
| Frontend Hasil | 0 | 1 | 0 | Diisi setelah UAT |
| REST API | 0 | 1 | 0 | Diisi setelah API test |
| Forward Chaining | 0 | 1 | 0 | Diisi setelah regression test |
| Knowledge Base | 0 | 1 | 0 | Diisi setelah validation review |

## Defect Life Cycle

| Bug ID | Modul | Severity | Priority | Status | Tanggal Open | Tanggal Closed | Root Cause |
|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - | - |

## Target Kualitas

| Metrik | Target | Status |
|---|---:|---|
| Line Coverage | >= 75% | Terpenuhi - 80,75% |
| API Error Rate Load Test | < 1% | Pending |
| API Error Rate Stress Test | < 5% | Pending |
| Response Time P95 Load Test | < 1000 ms | Pending |
| Response Time P95 Stress Test | < 2000 ms | Pending |
| Rata-rata SUS | >= 68 | Pending |
