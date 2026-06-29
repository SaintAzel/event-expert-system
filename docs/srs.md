# Software Requirements Specification (SRS)

## Event Expert System - Evalio

| Informasi | Keterangan |
| --- | --- |
| Nama Sistem | Evalio - Event Expert System |
| Judul | Sistem Pakar Penentuan Tingkat Kesiapan Penyelenggaraan Event Berdasarkan Faktor Risiko Menggunakan Metode Forward Chaining |
| Versi Dokumen | 1.0.0 |
| Versi Sistem | 1.0.0 |
| Versi Knowledge Base | 1.0.0 |
| Metode | Forward Chaining |
| Bahasa Dokumen | Indonesia |
| Tanggal Penyusunan | 29 Juni 2026 |

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen Software Requirements Specification (SRS) ini menjelaskan kebutuhan perangkat lunak untuk sistem Evalio, yaitu sistem pakar yang digunakan untuk menilai tingkat kesiapan penyelenggaraan event berdasarkan faktor risiko. Dokumen ini menjadi acuan bagi pengembang, penguji, pengguna, dan pihak terkait dalam memahami fungsi, batasan, kebutuhan data, serta perilaku sistem.

### 1.2 Ruang Lingkup Sistem

Evalio membantu pengguna mengevaluasi kesiapan event melalui checklist fakta yang dikelompokkan ke dalam beberapa kategori penilaian. Sistem memproses jawaban pengguna menggunakan metode forward chaining untuk menghasilkan:

- keputusan akhir kesiapan event;
- skor atau persentase kesiapan;
- tingkat risiko;
- penjelasan hasil inferensi;
- rekomendasi perbaikan terhadap aspek yang belum terpenuhi.

Sistem terdiri dari backend API berbasis FastAPI dan frontend berbasis HTML, CSS, dan JavaScript.

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Definisi |
| --- | --- |
| SRS | Software Requirements Specification, dokumen spesifikasi kebutuhan perangkat lunak. |
| Sistem Pakar | Sistem yang meniru proses pengambilan keputusan seorang pakar berdasarkan basis pengetahuan dan aturan. |
| Forward Chaining | Metode inferensi yang dimulai dari fakta yang diketahui untuk menghasilkan kesimpulan. |
| Fact | Fakta atau kondisi event yang dipilih pengguna melalui checklist. |
| Criteria | Kriteria kesiapan yang dihasilkan jika sejumlah fakta memenuhi aturan kategori. |
| Rule | Aturan logika yang menghubungkan fakta, kriteria, dan keputusan. |
| Decision | Keputusan akhir sistem terhadap kesiapan event. |
| Knowledge Base | Kumpulan fakta, kategori, kriteria, aturan, keputusan, dan rekomendasi. |

### 1.4 Referensi

- `README.md`
- `docs/knowledge_specification.md`
- `docs/knowledge_matrix.md`
- Knowledge repository pada `backend/src/event_expert/modules/knowledge/repository/`

## 2. Deskripsi Umum

### 2.1 Perspektif Produk

Evalio merupakan aplikasi evaluasi kesiapan event yang berjalan sebagai sistem web. Frontend menyediakan antarmuka checklist dan halaman hasil evaluasi. Backend menyediakan API untuk memproses fakta yang dipilih pengguna, menjalankan inferensi forward chaining, menghitung skor, dan mengembalikan hasil evaluasi.

### 2.2 Fungsi Utama Sistem

Sistem harus mampu:

- menampilkan daftar kategori dan pertanyaan evaluasi event;
- menerima pilihan fakta dari pengguna;
- memvalidasi minimal satu fakta sebelum evaluasi;
- menjalankan inferensi forward chaining berdasarkan knowledge base;
- menentukan kriteria yang terpenuhi dan tidak terpenuhi;
- menentukan keputusan akhir berupa READY, IMPROVEMENT, atau NOT_READY;
- menghitung persentase kesiapan dan tingkat risiko;
- menampilkan penjelasan hasil evaluasi;
- menampilkan rekomendasi perbaikan;
- menyimpan hasil evaluasi sementara di browser untuk ditampilkan pada halaman hasil;
- menyediakan opsi evaluasi ulang dan cetak laporan hasil.

### 2.3 Karakteristik Pengguna

| Pengguna | Deskripsi | Kebutuhan Utama |
| --- | --- | --- |
| Penyelenggara Event | Pihak yang merencanakan dan menjalankan event. | Mengetahui kesiapan event dan aspek yang harus diperbaiki. |
| Panitia Event | Tim operasional yang mengisi checklist kesiapan. | Mengisi kondisi aktual event secara cepat dan jelas. |
| Evaluator atau Pengawas | Pihak yang meninjau kelayakan event. | Melihat skor, risiko, keputusan, dan rekomendasi. |
| Pengembang Sistem | Pihak yang mengembangkan dan memelihara aplikasi. | Memastikan aturan, data, API, dan UI konsisten. |

### 2.4 Lingkungan Operasional

Backend:

- Python 3.13;
- FastAPI;
- Pydantic;
- Uvicorn;
- knowledge repository berbasis file JSON.

Frontend:

- HTML, CSS, dan JavaScript;
- browser modern;
- localStorage untuk penyimpanan hasil sementara;
- akses API backend pada `http://127.0.0.1:8000/evaluation`.

### 2.5 Batasan Sistem

- Sistem menggunakan basis pengetahuan statis berbasis JSON.
- Sistem belum menyediakan autentikasi pengguna.
- Sistem belum menyediakan penyimpanan riwayat evaluasi ke database.
- Frontend saat ini membaca daftar pertanyaan dari file JSON lokal.
- Evaluasi kesiapan bergantung pada fakta yang dipilih pengguna.
- Hasil sistem bersifat pendukung keputusan dan tidak menggantikan penilaian resmi dari otoritas terkait.

### 2.6 Asumsi dan Ketergantungan

- Pengguna memahami kondisi aktual event yang dievaluasi.
- Backend API berjalan dan dapat diakses oleh frontend.
- Knowledge base telah tervalidasi dan konsisten dengan spesifikasi pengetahuan.
- Browser pengguna mendukung JavaScript dan localStorage.

## 3. Kebutuhan Fungsional

### 3.1 Modul Landing Page

| ID | Kebutuhan |
| --- | --- |
| FR-001 | Sistem harus menampilkan halaman awal dengan identitas aplikasi Evalio. |
| FR-002 | Sistem harus menyediakan tombol untuk memulai evaluasi. |
| FR-003 | Sistem harus menampilkan ringkasan nilai utama aplikasi, seperti jumlah kategori penilaian dan hasil evaluasi yang cepat. |

### 3.2 Modul Checklist Evaluasi

| ID | Kebutuhan |
| --- | --- |
| FR-004 | Sistem harus menampilkan kategori penilaian event. |
| FR-005 | Sistem harus menampilkan pertanyaan checklist berdasarkan fakta pada setiap kategori. |
| FR-006 | Sistem harus memungkinkan pengguna memilih atau membatalkan pilihan fakta. |
| FR-007 | Sistem harus menampilkan jumlah fakta yang dipilih pada setiap kategori. |
| FR-008 | Sistem harus menampilkan progress evaluasi berdasarkan kategori yang sudah ditinjau. |
| FR-009 | Sistem harus memvalidasi bahwa minimal satu fakta dipilih sebelum evaluasi dijalankan. |
| FR-010 | Sistem harus membentuk payload evaluasi berisi daftar ID fakta yang dipilih pengguna. |

### 3.3 Modul Evaluasi Backend

| ID | Kebutuhan |
| --- | --- |
| FR-011 | Sistem harus menerima permintaan evaluasi melalui endpoint `POST /evaluation`. |
| FR-012 | Sistem harus menerima data fakta dalam bentuk daftar ID fakta. |
| FR-013 | Sistem harus memuat knowledge base sebelum proses evaluasi. |
| FR-014 | Sistem harus menjalankan forward chaining dari fakta menuju kriteria kategori. |
| FR-015 | Sistem harus menjalankan forward chaining dari kriteria menuju keputusan akhir. |
| FR-016 | Sistem harus menghasilkan daftar fakta yang dipicu, kriteria terpenuhi, kriteria belum terpenuhi, aturan yang cocok, dan waktu eksekusi inferensi. |
| FR-017 | Sistem harus mengembalikan respons evaluasi dalam format JSON. |

### 3.4 Modul Penentuan Keputusan

| ID | Kebutuhan |
| --- | --- |
| FR-018 | Sistem harus menghasilkan keputusan READY jika seluruh kriteria terpenuhi. |
| FR-019 | Sistem harus menghasilkan keputusan IMPROVEMENT jika kriteria kritis terpenuhi tetapi sebagian kriteria non-kritis belum terpenuhi. |
| FR-020 | Sistem harus menghasilkan keputusan NOT_READY jika kriteria kritis perizinan, venue, keamanan, atau medis tidak terpenuhi. |
| FR-021 | Sistem harus menggunakan keputusan default NOT_READY jika tidak ada global rule yang cocok. |

### 3.5 Modul Skor dan Risiko

| ID | Kebutuhan |
| --- | --- |
| FR-022 | Sistem harus menghitung persentase kesiapan berdasarkan jumlah kriteria terpenuhi dibanding total kriteria. |
| FR-023 | Sistem harus menentukan risiko LOW jika persentase kesiapan minimal 90%. |
| FR-024 | Sistem harus menentukan risiko MEDIUM jika persentase kesiapan minimal 70% dan kurang dari 90%. |
| FR-025 | Sistem harus menentukan risiko HIGH jika persentase kesiapan kurang dari 70%. |

### 3.6 Modul Penjelasan

| ID | Kebutuhan |
| --- | --- |
| FR-026 | Sistem harus menyediakan ringkasan hasil evaluasi dalam bentuk teks yang mudah dipahami. |
| FR-027 | Sistem harus menampilkan kriteria yang terpenuhi. |
| FR-028 | Sistem harus menampilkan kriteria yang belum terpenuhi. |
| FR-029 | Sistem harus menampilkan aturan yang cocok selama proses inferensi. |

### 3.7 Modul Rekomendasi

| ID | Kebutuhan |
| --- | --- |
| FR-030 | Sistem harus menghasilkan rekomendasi berdasarkan kriteria yang belum terpenuhi. |
| FR-031 | Sistem harus menampilkan rekomendasi beserta prioritasnya. |
| FR-032 | Sistem harus menghitung total rekomendasi yang diberikan. |

### 3.8 Modul Hasil Evaluasi

| ID | Kebutuhan |
| --- | --- |
| FR-033 | Sistem harus menyimpan hasil evaluasi sementara di localStorage browser. |
| FR-034 | Sistem harus menampilkan keputusan akhir pada halaman hasil. |
| FR-035 | Sistem harus menampilkan skor kesiapan, jumlah fakta terpenuhi, jumlah kategori atau kriteria terpenuhi, dan tingkat risiko. |
| FR-036 | Sistem harus menampilkan daftar rekomendasi perbaikan. |
| FR-037 | Sistem harus menyediakan tombol untuk memulai evaluasi baru. |
| FR-038 | Sistem harus menyediakan fitur cetak atau unduh laporan melalui fungsi print browser. |

### 3.9 Modul Sistem dan Health Check

| ID | Kebutuhan |
| --- | --- |
| FR-039 | Sistem harus menyediakan endpoint root yang mengembalikan nama API dan versi. |
| FR-040 | Sistem harus menyediakan endpoint versi yang mengembalikan versi API dan knowledge base. |
| FR-041 | Sistem harus menyediakan endpoint health check untuk memeriksa status layanan. |

## 4. Kebutuhan Data dan Knowledge Base

### 4.1 Komponen Knowledge Base

| Komponen | Jumlah | Keterangan |
| --- | ---: | --- |
| Kategori | 8 | Area evaluasi kesiapan event. |
| Fakta | 40 | Kondisi event yang dipilih pengguna. |
| Kriteria | 8 | Hasil evaluasi setiap kategori. |
| Category Rules | 8 | Aturan dari fakta menuju kriteria. |
| Global Rules | 6 | Aturan dari kriteria menuju keputusan akhir. |
| Keputusan | 3 | READY, IMPROVEMENT, NOT_READY. |
| Rekomendasi | 8 | Saran perbaikan berdasarkan kriteria yang belum terpenuhi. |

### 4.2 Kategori Penilaian

| ID | Kategori | Prioritas |
| --- | --- | --- |
| C01 | Perizinan | Critical |
| C02 | Venue | Critical |
| C03 | Sumber Daya Manusia | High |
| C04 | Keamanan | Critical |
| C05 | Medis | Critical |
| C06 | Logistik | High |
| C07 | Operasional | High |
| C08 | Komunikasi | Medium |

### 4.3 Aturan Kategori

| Rule | Kondisi | Hasil |
| --- | --- | --- |
| CR001 | F001 dan F002 dan F005 | RC01 |
| CR002 | F006 dan F007 dan F008 | RC02 |
| CR003 | F011 dan F012 | RC03 |
| CR004 | F016 dan F017 dan F019 dan F020 | RC04 |
| CR005 | F021 dan F022 dan F024 | RC05 |
| CR006 | F027 dan F030 | RC06 |
| CR007 | F031 dan F032 | RC07 |
| CR008 | F036 dan F038 | RC08 |

### 4.4 Aturan Keputusan Global

| Rule | Kondisi | Keputusan |
| --- | --- | --- |
| GR001 | RC01, RC02, RC03, RC04, RC05, RC06, RC07, RC08 terpenuhi | READY |
| GR002 | RC01, RC02, RC04, RC05 terpenuhi, tetapi salah satu RC03, RC06, RC07, atau RC08 belum terpenuhi | IMPROVEMENT |
| GR003 | RC01 tidak terpenuhi | NOT_READY |
| GR004 | RC02 tidak terpenuhi | NOT_READY |
| GR005 | RC04 tidak terpenuhi | NOT_READY |
| GR006 | RC05 tidak terpenuhi | NOT_READY |

### 4.5 Keputusan Akhir

| Keputusan | Deskripsi |
| --- | --- |
| READY | Event siap diselenggarakan karena seluruh aspek utama telah terpenuhi. |
| IMPROVEMENT | Event dapat diselenggarakan setelah beberapa aspek non-kritis diperbaiki. |
| NOT_READY | Event belum layak diselenggarakan karena terdapat aspek kritis yang belum terpenuhi. |

## 5. Kebutuhan Antarmuka Eksternal

### 5.1 Antarmuka Pengguna

Sistem harus menyediakan tiga halaman utama:

- halaman awal untuk pengenalan aplikasi dan akses evaluasi;
- halaman evaluasi untuk checklist kesiapan event;
- halaman hasil untuk menampilkan keputusan, skor, risiko, penjelasan, rekomendasi, dan opsi cetak.

### 5.2 Antarmuka API

#### POST `/evaluation`

Deskripsi: menjalankan evaluasi kesiapan event berdasarkan fakta yang dipilih pengguna.

Contoh request:

```json
{
  "facts": ["F001", "F002", "F005", "F006"]
}
```

Contoh struktur response:

```json
{
  "success": true,
  "message": "Evaluation completed successfully.",
  "data": {
    "inference": {},
    "explanation": {},
    "recommendation": {},
    "evaluation": {}
  }
}
```

#### GET `/`

Deskripsi: mengembalikan informasi dasar API.

#### GET `/version`

Deskripsi: mengembalikan versi API dan knowledge base.

### 5.3 Antarmuka Penyimpanan

Frontend menggunakan localStorage untuk menyimpan hasil evaluasi sementara dengan data:

- request fakta yang dikirim;
- response evaluasi dari backend;
- waktu evaluasi.

## 6. Kebutuhan Non-Fungsional

### 6.1 Kinerja

| ID | Kebutuhan |
| --- | --- |
| NFR-001 | Proses inferensi harus dapat dijalankan secara cepat untuk 40 fakta, 8 kriteria, dan 14 aturan. |
| NFR-002 | API evaluasi sebaiknya merespons dalam waktu kurang dari 2 detik pada lingkungan lokal normal. |
| NFR-003 | Halaman hasil harus dapat ditampilkan segera setelah response evaluasi diterima. |

### 6.2 Keandalan

| ID | Kebutuhan |
| --- | --- |
| NFR-004 | Sistem harus tetap menghasilkan keputusan default NOT_READY jika tidak ada global rule yang cocok. |
| NFR-005 | Sistem harus menolak atau menangani ID fakta yang tidak valid sesuai validasi skema. |
| NFR-006 | Sistem harus menampilkan pesan kegagalan jika frontend tidak dapat menghubungi backend. |

### 6.3 Kegunaan

| ID | Kebutuhan |
| --- | --- |
| NFR-007 | Antarmuka harus mudah digunakan oleh pengguna non-teknis. |
| NFR-008 | Pertanyaan checklist harus ditampilkan per kategori agar mudah dipahami. |
| NFR-009 | Hasil evaluasi harus disajikan dengan label keputusan, skor, risiko, dan rekomendasi yang jelas. |

### 6.4 Pemeliharaan

| ID | Kebutuhan |
| --- | --- |
| NFR-010 | Knowledge base harus dipisahkan dari kode program agar mudah diperbarui. |
| NFR-011 | Setiap komponen knowledge base harus mengikuti format ID yang konsisten. |
| NFR-012 | Backend harus memisahkan modul knowledge, inference, explanation, recommendation, evaluation, dan API. |

### 6.5 Keamanan

| ID | Kebutuhan |
| --- | --- |
| NFR-013 | API harus melakukan validasi request menggunakan skema data. |
| NFR-014 | CORS harus dibatasi pada origin frontend yang diizinkan. |
| NFR-015 | Sistem tidak boleh menyimpan data sensitif pengguna tanpa mekanisme keamanan tambahan. |

### 6.6 Portabilitas

| ID | Kebutuhan |
| --- | --- |
| NFR-016 | Backend harus dapat dijalankan pada lingkungan yang mendukung Python 3.13. |
| NFR-017 | Frontend harus dapat dijalankan pada browser modern. |

## 7. Model Proses Sistem

Alur utama evaluasi:

1. Pengguna membuka halaman Evalio.
2. Pengguna memilih menu mulai evaluasi.
3. Sistem menampilkan checklist berdasarkan kategori.
4. Pengguna memilih fakta yang sesuai dengan kondisi event.
5. Frontend mengirim daftar ID fakta ke backend.
6. Backend memuat knowledge base.
7. Forward chaining mencocokkan fakta dengan category rules.
8. Sistem menghasilkan kriteria yang terpenuhi.
9. Forward chaining mencocokkan kriteria dengan global rules.
10. Sistem menghasilkan keputusan akhir.
11. Sistem menghitung skor kesiapan dan tingkat risiko.
12. Sistem menghasilkan penjelasan dan rekomendasi.
13. Frontend menyimpan hasil sementara dan menampilkan halaman hasil.

## 8. Kriteria Penerimaan

| ID | Kriteria |
| --- | --- |
| AC-001 | Pengguna dapat membuka halaman awal dan berpindah ke halaman evaluasi. |
| AC-002 | Pengguna dapat melihat 8 kategori penilaian. |
| AC-003 | Pengguna dapat memilih fakta pada setiap kategori. |
| AC-004 | Sistem menolak evaluasi jika tidak ada fakta yang dipilih. |
| AC-005 | Sistem mengirim payload fakta ke endpoint `POST /evaluation`. |
| AC-006 | Backend mengembalikan hasil evaluasi dengan struktur inference, explanation, recommendation, dan evaluation. |
| AC-007 | Jika seluruh kriteria terpenuhi, keputusan akhir adalah READY. |
| AC-008 | Jika kriteria kritis terpenuhi tetapi ada kriteria non-kritis yang belum terpenuhi, keputusan akhir adalah IMPROVEMENT. |
| AC-009 | Jika perizinan, venue, keamanan, atau medis tidak terpenuhi, keputusan akhir adalah NOT_READY. |
| AC-010 | Sistem menampilkan rekomendasi untuk setiap kriteria yang belum terpenuhi. |
| AC-011 | Sistem menampilkan skor kesiapan dan tingkat risiko. |
| AC-012 | Pengguna dapat melakukan evaluasi baru dari halaman hasil. |
| AC-013 | Pengguna dapat mencetak laporan hasil evaluasi. |

## 9. Kebutuhan Pengujian

Pengujian minimal yang perlu dilakukan:

- pengujian validasi knowledge base;
- pengujian forward chaining untuk skenario READY;
- pengujian forward chaining untuk skenario IMPROVEMENT;
- pengujian forward chaining untuk skenario NOT_READY;
- pengujian endpoint `POST /evaluation`;
- pengujian tampilan checklist pada frontend;
- pengujian penyimpanan hasil ke localStorage;
- pengujian halaman hasil dan cetak laporan.

## 10. Prioritas Pengembangan Lanjutan

Beberapa pengembangan yang dapat dipertimbangkan:

- endpoint khusus untuk mengambil knowledge base agar frontend tidak bergantung pada JSON lokal;
- penyimpanan riwayat evaluasi ke database;
- autentikasi dan otorisasi pengguna;
- dashboard admin untuk mengelola fakta, aturan, dan rekomendasi;
- ekspor laporan ke PDF;
- validasi bukti dokumen untuk setiap fakta;
- dukungan multi-event dan multi-user.

## 11. Lampiran Ringkas Rekomendasi

| Kriteria | Rekomendasi |
| --- | --- |
| RC01 | Lengkapi seluruh dokumen perizinan. |
| RC02 | Pastikan venue memenuhi kapasitas dan memiliki jalur evakuasi. |
| RC03 | Lengkapi struktur organisasi dan pembagian tugas panitia. |
| RC04 | Lengkapi sistem keamanan, APAR, dan prosedur evakuasi. |
| RC05 | Sediakan tim medis, ambulans, dan perlengkapan P3K. |
| RC06 | Lengkapi logistik utama dan sumber listrik cadangan. |
| RC07 | Finalisasi SOP, rundown, dan kesiapan operasional. |
| RC08 | Tingkatkan komunikasi internal dan penyampaian informasi kepada peserta. |
