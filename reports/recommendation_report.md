# Rekomendasi Kualitas Perangkat Lunak - Evalio

## Ringkasan

Evalio dinyatakan production ready berdasarkan asumsi proyek. Rekomendasi berikut difokuskan pada penguatan proses SQA, observabilitas, keamanan operasional, dan dokumentasi pengujian tanpa mengubah source code, UI, business logic, endpoint, JSON knowledge base, atau arsitektur.

## Matriks Rekomendasi

| Area | Temuan/Risiko | Rekomendasi | Prioritas | Dampak |
|---|---|---|---|---|
| Regression Testing | Perubahan rule atau knowledge base berpotensi mengubah keputusan akhir. | Jalankan pytest setiap pull request dan simpan bukti coverage. | High | Menjaga konsistensi keputusan READY/IMPROVEMENT/NOT_READY |
| API Reliability | Endpoint `/evaluation` menjadi pusat seluruh proses evaluasi. | Jalankan k6 load test sebelum rilis dan catat P95, error rate, throughput. | High | Mengurangi risiko penurunan performa |
| Security Operations | Aplikasi publik dapat menerima request berulang. | Terapkan rate limiting pada reverse proxy/API gateway produksi. | High | Mengurangi risiko abuse tanpa mengubah aplikasi |
| Dependency Security | Dependency dapat memiliki vulnerability baru setelah rilis. | Jalankan `pip-audit` berkala dan dokumentasikan hasilnya. | High | Mendeteksi risiko library lebih awal |
| Usability | Pengguna perlu memahami kategori dan fakta kesiapan event. | Lakukan SUS minimal tiga responden setiap iterasi rilis. | Medium | Mengukur kemudahan penggunaan secara kuantitatif |
| Documentation | Bukti eksekusi pengujian perlu siap untuk audit akademik. | Simpan screenshot hasil pytest coverage, k6 summary, pip-audit, dan SUS. | Medium | Memperkuat validitas laporan |
| Defect Management | Bug perlu dilacak dengan status formal. | Gunakan template bug report dan defect life cycle. | Medium | Memudahkan retest dan penutupan defect |

## Rekomendasi Eksekusi Sebelum Pengumpulan

1. Jalankan `pytest` dan simpan screenshot coverage terminal serta folder `reports/coverage_html`.
2. Jalankan aplikasi backend lokal pada `http://127.0.0.1:8000`.
3. Jalankan `k6 run performance/evaluation-load-test.js`.
4. Jalankan `k6 run performance/evaluation-stress-test.js`.
5. Jalankan `pip-audit -r backend/requirements.txt`.
6. Eksekusi UAT manual berdasarkan `docs/testing/uat_scenarios.md`.
7. Minta minimal tiga responden mengisi SUS.
8. Lengkapi `docs/testing/quality_metrics_template.md` berdasarkan hasil aktual.

## Pernyataan Batasan

Rekomendasi ini tidak meminta perubahan implementasi karena proyek telah dianggap selesai dan production ready. Setiap usulan teknis yang menyentuh runtime produksi ditempatkan sebagai rekomendasi operasional atau deployment-level control.
