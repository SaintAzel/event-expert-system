# User Acceptance Test (UAT) - Evalio

## Identitas Pengujian

- Nama aplikasi: Evalio - Event Readiness Expert System
- Peran penguji: Pengguna akhir/panitia event
- Tujuan UAT: Memastikan alur evaluasi kesiapan event dapat digunakan untuk mengambil keputusan READY, IMPROVEMENT, atau NOT_READY sesuai fakta yang dipilih pengguna.
- Status awal: Aplikasi dianggap production ready dan implementasi telah disetujui.

## Tabel Skenario UAT

| ID Skenario | Skenario | Deskripsi Langkah Pengujian | Expected Result | Status |
|---|---|---|---|---|
| UAT-EVL-01 | Membuka halaman awal aplikasi | 1. Buka `frontend/index.html`. 2. Amati tampilan awal. 3. Klik tombol mulai evaluasi. | Sistem menampilkan halaman awal Evalio dan mengarahkan pengguna ke halaman evaluasi. | Pending |
| UAT-EVL-02 | Memuat daftar kategori kesiapan event | 1. Buka halaman evaluasi. 2. Tunggu proses pemuatan data knowledge. 3. Amati daftar kategori. | Sistem menampilkan kategori perizinan, venue, SDM, keamanan, medis, logistik, operasional, dan komunikasi. | Pending |
| UAT-EVL-03 | Evaluasi event dengan semua fakta kritikal terpenuhi | 1. Pilih seluruh fakta wajib pada setiap kategori. 2. Klik tombol evaluasi. 3. Tunggu hasil. | Sistem menyimpan hasil evaluasi dan menampilkan keputusan READY dengan risiko LOW. | Pending |
| UAT-EVL-04 | Evaluasi event dengan satu kategori belum lengkap | 1. Pilih fakta pada tujuh kategori utama. 2. Kosongkan fakta pada kategori komunikasi. 3. Klik tombol evaluasi. | Sistem menampilkan keputusan IMPROVEMENT dan rekomendasi untuk kategori yang belum lengkap. | Pending |
| UAT-EVL-05 | Evaluasi event tanpa fakta terpenuhi | 1. Buka halaman evaluasi. 2. Jangan pilih fakta kesiapan. 3. Klik tombol evaluasi. | Sistem memblokir atau memberi pesan bahwa evaluasi belum dapat dilanjutkan karena input belum lengkap, sesuai validasi UI yang ada. | Pending |
| UAT-EVL-06 | Melihat ringkasan hasil evaluasi | 1. Selesaikan evaluasi valid. 2. Buka halaman hasil. 3. Amati skor, keputusan, risiko, dan rekomendasi. | Sistem menampilkan ringkasan hasil yang konsisten dengan response API. | Pending |
| UAT-EVL-07 | Memulai evaluasi ulang | 1. Buka halaman hasil setelah evaluasi. 2. Klik tombol evaluasi baru. | Sistem kembali ke halaman evaluasi untuk pengisian ulang. | Pending |
| UAT-EVL-08 | Backend API tidak berjalan | 1. Matikan backend. 2. Isi data evaluasi valid. 3. Klik evaluasi. | Sistem menampilkan pesan gagal evaluasi dan tidak mengubah perilaku aplikasi. | Pending |
| UAT-EVL-09 | Validasi endpoint health | 1. Akses `GET /health`. 2. Periksa respons. | API mengembalikan `status: ok` dan service `event-expert-system`. | Pending |
| UAT-EVL-10 | Validasi format fakta tidak valid | 1. Kirim `POST /evaluation` dengan `facts: ["INVALID_FACT"]`. 2. Amati respons API. | API menolak payload dengan status validasi 422. | Pending |

## Catatan Eksekusi

Kolom status diisi setelah pengujian manual: Pass, Fail, atau Pending. Jika terdapat status Fail, buat laporan cacat terpisah menggunakan template pada `docs/testing/bug_report_template.md`.
