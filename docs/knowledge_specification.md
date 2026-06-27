# Knowledge Specification Document

## Event Expert System Knowledge Specification (ESKS) v1.0

---

# Document Information

| Item              | Value                                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Project           | Event Expert System                                                                                                         |
| Title             | Sistem Pakar Penentuan Tingkat Kesiapan Penyelenggaraan Event Berdasarkan Faktor Risiko Menggunakan Metode Forward Chaining |
| Version           | 1.0.0                                                                                                                       |
| Knowledge Version | 1.0.0                                                                                                                       |
| Method            | Forward Chaining                                                                                                            |
| Status            | Approved                                                                                                                    |
| Author            | Ahmad Guffran                                                                                                               |
| Last Updated      | 27 June 2026                                                                                                                |

---

# 1. Purpose

Dokumen ini mendefinisikan seluruh knowledge yang digunakan oleh sistem pakar.

Dokumen ini menjadi sumber utama (Single Source of Truth) bagi seluruh implementasi backend.

Seluruh komponen berikut harus konsisten dengan dokumen ini:

* Knowledge Repository
* Repository Validator
* Knowledge Loader
* Forward Chaining Engine
* Explanation Engine
* Recommendation Engine
* REST API
* User Interface Questionnaire

---

# 2. Knowledge Architecture

```text
User Answer
      │
      ▼
Facts (F001-F040)
      │
      ▼
Category Rules (CR001-CR008)
      │
      ▼
Criteria (RC01-RC08)
      │
      ▼
Global Rules (GR001-GR006)
      │
      ▼
Decision
      │
      ▼
Recommendation
```

---

# 3. Knowledge Components

## Categories

| ID  | Category            | Priority |
| --- | ------------------- | -------- |
| C01 | Perizinan           | Critical |
| C02 | Venue               | Critical |
| C03 | Sumber Daya Manusia | High     |
| C04 | Keamanan            | Critical |
| C05 | Medis               | Critical |
| C06 | Logistik            | High     |
| C07 | Operasional         | High     |
| C08 | Komunikasi          | Medium   |

---

# 4. Knowledge Traceability Matrix

Setiap fakta memiliki hubungan langsung terhadap:

* Pertanyaan yang ditampilkan kepada pengguna.
* Bukti yang harus dipenuhi.
* Rule yang menggunakannya.
* Criteria yang dihasilkan.
* Recommendation yang diberikan apabila criteria tidak terpenuhi.

---

## C01 — Perizinan

| Fact ID | Question                                                          | Evidence                | Rule  | Criteria | Recommendation |
| ------- | ----------------------------------------------------------------- | ----------------------- | ----- | -------- | -------------- |
| F001    | Apakah izin keramaian telah diterbitkan?                          | Surat Izin Keramaian    | CR001 | RC01     | REC001         |
| F002    | Apakah izin penggunaan lokasi telah diterbitkan?                  | Surat Izin Lokasi       | CR001 | RC01     | REC001         |
| F003    | Apakah izin penggunaan jalan telah diterbitkan (jika diperlukan)? | Surat Izin Jalan        | -     | -        | -              |
| F004    | Apakah koordinasi dengan instansi terkait telah dilakukan?        | Berita Acara Koordinasi | -     | -        | -              |
| F005    | Apakah seluruh dokumen legal penyelenggaraan telah lengkap?       | Dokumen Legal           | CR001 | RC01     | REC001         |

---

## C02 — Venue

| Fact ID | Question                            | Evidence        | Rule  | Criteria | Recommendation |
| ------- | ----------------------------------- | --------------- | ----- | -------- | -------------- |
| F006    | Apakah venue telah ditentukan?      | Kontrak Venue   | CR002 | RC02     | REC002         |
| F007    | Apakah kapasitas venue sesuai?      | Layout Venue    | CR002 | RC02     | REC002         |
| F008    | Apakah jalur evakuasi tersedia?     | Denah Evakuasi  | CR002 | RC02     | REC002         |
| F009    | Apakah area parkir tersedia?        | Layout Parkir   | -     | -        | -              |
| F010    | Apakah fasilitas sanitasi tersedia? | Checklist Venue | -     | -        | -              |

---

## C03 — Sumber Daya Manusia

| Fact ID | Question                                    | Evidence              | Rule  | Criteria | Recommendation |
| ------- | ------------------------------------------- | --------------------- | ----- | -------- | -------------- |
| F011    | Apakah ketua panitia telah ditetapkan?      | SK Panitia            | CR003 | RC03     | REC003         |
| F012    | Apakah struktur kepanitiaan telah lengkap?  | Struktur Organisasi   | CR003 | RC03     | REC003         |
| F013    | Apakah jobdesk setiap divisi telah disusun? | Dokumen Jobdesk       | -     | -        | -              |
| F014    | Apakah jumlah relawan mencukupi?            | Daftar Relawan        | -     | -        | -              |
| F015    | Apakah briefing panitia telah dilakukan?    | Berita Acara Briefing | -     | -        | -              |

---

## C04 — Keamanan

| Fact ID | Question                                    | Evidence         | Rule  | Criteria | Recommendation |
| ------- | ------------------------------------------- | ---------------- | ----- | -------- | -------------- |
| F016    | Apakah petugas keamanan tersedia?           | Daftar Petugas   | CR004 | RC04     | REC004         |
| F017    | Apakah APAR tersedia?                       | Checklist APAR   | CR004 | RC04     | REC004         |
| F018    | Apakah CCTV tersedia?                       | Dokumentasi CCTV | -     | -        | -              |
| F019    | Apakah jalur evakuasi telah diberi penanda? | Denah Evakuasi   | CR004 | RC04     | REC004         |
| F020    | Apakah SOP keadaan darurat tersedia?        | SOP Darurat      | CR004 | RC04     | REC004         |

---

## C05 — Medis

| Fact ID | Question                                     | Evidence              | Rule  | Criteria | Recommendation |
| ------- | -------------------------------------------- | --------------------- | ----- | -------- | -------------- |
| F021    | Apakah tim medis tersedia?                   | Surat Tugas Tim Medis | CR005 | RC05     | REC005         |
| F022    | Apakah ambulans tersedia?                    | Kontrak Ambulans      | CR005 | RC05     | REC005         |
| F023    | Apakah pos kesehatan tersedia?               | Layout Pos Kesehatan  | -     | -        | -              |
| F024    | Apakah perlengkapan P3K tersedia?            | Checklist P3K         | CR005 | RC05     | REC005         |
| F025    | Apakah rumah sakit rujukan telah ditentukan? | Surat Kerja Sama      | -     | -        | -              |

---

## C06 — Logistik

| Fact ID | Question                                     | Evidence              | Rule  | Criteria | Recommendation |
| ------- | -------------------------------------------- | --------------------- | ----- | -------- | -------------- |
| F026    | Apakah peralatan utama tersedia?             | Checklist Logistik    | -     | -        | -              |
| F027    | Apakah sumber listrik utama tersedia?        | Checklist Kelistrikan | CR006 | RC06     | REC006         |
| F028    | Apakah genset cadangan tersedia?             | Checklist Genset      | -     | -        | -              |
| F029    | Apakah meja registrasi tersedia?             | Checklist Registrasi  | -     | -        | -              |
| F030    | Apakah seluruh peralatan pendukung tersedia? | Checklist Peralatan   | CR006 | RC06     | REC006         |

---

## C07 — Operasional

| Fact ID | Question                                           | Evidence                  | Rule  | Criteria | Recommendation |
| ------- | -------------------------------------------------- | ------------------------- | ----- | -------- | -------------- |
| F031    | Apakah rundown telah disetujui?                    | Rundown Event             | CR007 | RC07     | REC007         |
| F032    | Apakah SOP operasional tersedia?                   | SOP Operasional           | CR007 | RC07     | REC007         |
| F033    | Apakah sistem registrasi peserta siap?             | Checklist Registrasi      | -     | -        | -              |
| F034    | Apakah gladi bersih telah dilakukan?               | Berita Acara Gladi Bersih | -     | -        | -              |
| F035    | Apakah penanggung jawab lapangan telah ditetapkan? | SK Penanggung Jawab       | -     | -        | -              |

---

## C08 — Komunikasi

| Fact ID | Question                                           | Evidence                   | Rule  | Criteria | Recommendation |
| ------- | -------------------------------------------------- | -------------------------- | ----- | -------- | -------------- |
| F036    | Apakah media komunikasi internal aktif?            | Grup Komunikasi            | CR008 | RC08     | REC008         |
| F037    | Apakah media partner telah ditetapkan?             | MoU Media Partner          | -     | -        | -              |
| F038    | Apakah informasi kepada peserta telah disampaikan? | Bukti Pengiriman Informasi | CR008 | RC08     | REC008         |
| F039    | Apakah kontak darurat tersedia?                    | Daftar Kontak Darurat      | -     | -        | -              |
| F040    | Apakah tim dokumentasi siap?                       | SK Tim Dokumentasi         | -     | -        | -              |

---

# 5. Category Rules

| Rule  | Logic                     | Result |
| ----- | ------------------------- | ------ |
| CR001 | F001 ∧ F002 ∧ F005        | RC01   |
| CR002 | F006 ∧ F007 ∧ F008        | RC02   |
| CR003 | F011 ∧ F012               | RC03   |
| CR004 | F016 ∧ F017 ∧ F019 ∧ F020 | RC04   |
| CR005 | F021 ∧ F022 ∧ F024        | RC05   |
| CR006 | F027 ∧ F030               | RC06   |
| CR007 | F031 ∧ F032               | RC07   |
| CR008 | F036 ∧ F038               | RC08   |

---

# 6. Global Rules

| Rule  | Logic                                                                                     | Decision    |
| ----- | ----------------------------------------------------------------------------------------- | ----------- |
| GR001 | RC01 ∧ RC02 ∧ RC03 ∧ RC04 ∧ RC05 ∧ RC06 ∧ RC07 ∧ RC08                                     | READY       |
| GR002 | RC01 ∧ RC02 ∧ RC04 ∧ RC05 terpenuhi, namun salah satu RC03/RC06/RC07/RC08 belum terpenuhi | IMPROVEMENT |
| GR003 | RC01 tidak terpenuhi                                                                      | NOT_READY   |
| GR004 | RC02 tidak terpenuhi                                                                      | NOT_READY   |
| GR005 | RC04 tidak terpenuhi                                                                      | NOT_READY   |
| GR006 | RC05 tidak terpenuhi                                                                      | NOT_READY   |

---

# 7. Decision Levels

| Decision    | Description                                                                          |
| ----------- | ------------------------------------------------------------------------------------ |
| READY       | Seluruh aspek utama telah memenuhi persyaratan.                                      |
| IMPROVEMENT | Event dapat diselenggarakan setelah beberapa aspek non-kritis diperbaiki.            |
| NOT_READY   | Event belum layak diselenggarakan karena terdapat aspek kritis yang belum terpenuhi. |

---

# 8. Recommendation Mapping

| Criteria | Recommendation                                            |
| -------- | --------------------------------------------------------- |
| RC01     | Lengkapi seluruh dokumen perizinan.                       |
| RC02     | Pastikan venue memenuhi seluruh persyaratan keselamatan.  |
| RC03     | Lengkapi struktur organisasi dan pembagian tugas panitia. |
| RC04     | Lengkapi sistem keamanan dan prosedur evakuasi.           |
| RC05     | Sediakan fasilitas medis sesuai standar.                  |
| RC06     | Lengkapi logistik dan sumber daya pendukung.              |
| RC07     | Finalisasi SOP dan operasional event.                     |
| RC08     | Tingkatkan komunikasi internal maupun eksternal.          |

---

# 9. Repository Mapping

| Document        | Repository File      |
| --------------- | -------------------- |
| Categories      | categories.json      |
| Facts           | facts.json           |
| Criteria        | criteria.json        |
| Category Rules  | category_rules.json  |
| Global Rules    | global_rules.json    |
| Recommendations | recommendations.json |
| Decisions       | decisions.json       |
| Metadata        | metadata.json        |

---

# 10. Knowledge Statistics

| Component       | Total |
| --------------- | ----: |
| Categories      |     8 |
| Facts           |    40 |
| Criteria        |     8 |
| Category Rules  |     8 |
| Global Rules    |     6 |
| Decisions       |     3 |
| Recommendations |     8 |

---

# Approval

Dokumen ini merupakan spesifikasi resmi Knowledge Base yang menjadi acuan seluruh implementasi backend. Setiap perubahan pada Knowledge Repository harus terlebih dahulu direfleksikan pada dokumen ini agar konsistensi antara desain dan implementasi tetap terjaga.
