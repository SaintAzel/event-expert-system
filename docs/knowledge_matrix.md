# Knowledge Matrix

## Event Expert System Knowledge Specification (ESKS) v1.0

**Project** : Event Expert System
**Title** : Sistem Pakar Penentuan Tingkat Kesiapan Penyelenggaraan Event Berdasarkan Faktor Risiko Menggunakan Metode Forward Chaining

---

# 1. Overview

Knowledge Matrix merupakan dokumen utama (Single Source of Truth) yang mendefinisikan hubungan antara seluruh komponen Knowledge Base pada sistem pakar.

Dokumen ini menjadi acuan dalam pembangunan:

* Knowledge Repository
* Knowledge Validator
* Knowledge Loader
* Forward Chaining Engine
* Explanation Engine
* Recommendation Engine

Seluruh file JSON pada folder `repository/` harus konsisten dengan dokumen ini.

---

# 2. Knowledge Architecture

```text
Facts
    │
    ▼
Category Rules
    │
    ▼
Criteria
    │
    ▼
Global Rules
    │
    ▼
Decision
```

---

# 3. Category Matrix

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

# 4. Knowledge Matrix

## C01 – Perizinan

| Fact | Nama Fakta                         | Critical | Rule  | Criteria |
| ---- | ---------------------------------- | -------- | ----- | -------- |
| F001 | Izin keramaian tersedia            | ✅        | CR001 | RC01     |
| F002 | Izin penggunaan lokasi tersedia    | ✅        | CR001 | RC01     |
| F003 | Izin penggunaan jalan tersedia     | ❌        | —     | —        |
| F004 | Koordinasi dengan instansi terkait | ❌        | —     | —        |
| F005 | Dokumen legal lengkap              | ✅        | CR001 | RC01     |

**Category Rule**

```text
IF F001 AND F002 AND F005
THEN RC01
```

---

## C02 – Venue

| Fact | Nama Fakta                  | Critical | Rule  | Criteria |
| ---- | --------------------------- | -------- | ----- | -------- |
| F006 | Venue telah ditentukan      | ✅        | CR002 | RC02     |
| F007 | Kapasitas venue mencukupi   | ✅        | CR002 | RC02     |
| F008 | Jalur evakuasi tersedia     | ✅        | CR002 | RC02     |
| F009 | Area parkir tersedia        | ❌        | —     | —        |
| F010 | Fasilitas sanitasi tersedia | ❌        | —     | —        |

**Category Rule**

```text
IF F006 AND F007 AND F008
THEN RC02
```

---

## C03 – Sumber Daya Manusia

| Fact | Nama Fakta                       | Critical | Rule  | Criteria |
| ---- | -------------------------------- | -------- | ----- | -------- |
| F011 | Ketua panitia telah ditetapkan   | ✅        | CR003 | RC03     |
| F012 | Struktur kepanitiaan lengkap     | ✅        | CR003 | RC03     |
| F013 | Jobdesk setiap divisi tersedia   | ❌        | —     | —        |
| F014 | Relawan mencukupi                | ❌        | —     | —        |
| F015 | Briefing panitia telah dilakukan | ❌        | —     | —        |

**Category Rule**

```text
IF F011 AND F012
THEN RC03
```

---

## C04 – Keamanan

| Fact | Nama Fakta                    | Critical | Rule  | Criteria |
| ---- | ----------------------------- | -------- | ----- | -------- |
| F016 | Petugas keamanan tersedia     | ✅        | CR004 | RC04     |
| F017 | APAR tersedia                 | ✅        | CR004 | RC04     |
| F018 | CCTV tersedia                 | ❌        | —     | —        |
| F019 | Jalur evakuasi diberi penanda | ✅        | CR004 | RC04     |
| F020 | SOP keadaan darurat tersedia  | ✅        | CR004 | RC04     |

**Category Rule**

```text
IF F016 AND F017 AND F019 AND F020
THEN RC04
```

---

## C05 – Medis

| Fact | Nama Fakta                     | Critical | Rule  | Criteria |
| ---- | ------------------------------ | -------- | ----- | -------- |
| F021 | Tim medis tersedia             | ✅        | CR005 | RC05     |
| F022 | Ambulans tersedia              | ✅        | CR005 | RC05     |
| F023 | Pos kesehatan tersedia         | ❌        | —     | —        |
| F024 | Peralatan P3K tersedia         | ✅        | CR005 | RC05     |
| F025 | Rumah sakit rujukan ditentukan | ❌        | —     | —        |

**Category Rule**

```text
IF F021 AND F022 AND F024
THEN RC05
```

---

## C06 – Logistik

| Fact | Nama Fakta                   | Critical | Rule  | Criteria |
| ---- | ---------------------------- | -------- | ----- | -------- |
| F026 | Peralatan utama tersedia     | ❌        | —     | —        |
| F027 | Listrik utama tersedia       | ✅        | CR006 | RC06     |
| F028 | Genset tersedia              | ❌        | —     | —        |
| F029 | Meja registrasi tersedia     | ❌        | —     | —        |
| F030 | Peralatan pendukung tersedia | ✅        | CR006 | RC06     |

**Category Rule**

```text
IF F027 AND F030
THEN RC06
```

---

## C07 – Operasional

| Fact | Nama Fakta                         | Critical | Rule  | Criteria |
| ---- | ---------------------------------- | -------- | ----- | -------- |
| F031 | Rundown disetujui                  | ✅        | CR007 | RC07     |
| F032 | SOP operasional tersedia           | ✅        | CR007 | RC07     |
| F033 | Registrasi peserta siap            | ❌        | —     | —        |
| F034 | Gladi bersih selesai               | ❌        | —     | —        |
| F035 | Penanggung jawab lapangan tersedia | ❌        | —     | —        |

**Category Rule**

```text
IF F031 AND F032
THEN RC07
```

---

## C08 – Komunikasi

| Fact | Nama Fakta                          | Critical | Rule  | Criteria |
| ---- | ----------------------------------- | -------- | ----- | -------- |
| F036 | Media komunikasi internal aktif     | ✅        | CR008 | RC08     |
| F037 | Media partner tersedia              | ❌        | —     | —        |
| F038 | Informasi peserta telah disampaikan | ✅        | CR008 | RC08     |
| F039 | Kontak darurat tersedia             | ❌        | —     | —        |
| F040 | Dokumentasi siap                    | ❌        | —     | —        |

**Category Rule**

```text
IF F036 AND F038
THEN RC08
```

---

# 5. Global Rule Matrix

| Rule  | Conditions                                                                                    | Decision    |
| ----- | --------------------------------------------------------------------------------------------- | ----------- |
| GR001 | RC01 + RC02 + RC03 + RC04 + RC05 + RC06 + RC07 + RC08                                         | READY       |
| GR002 | RC01 + RC02 + RC04 + RC05 terpenuhi, namun RC03 atau RC06 atau RC07 atau RC08 belum terpenuhi | IMPROVEMENT |
| GR003 | RC01 tidak terpenuhi                                                                          | NOT_READY   |
| GR004 | RC02 tidak terpenuhi                                                                          | NOT_READY   |
| GR005 | RC04 tidak terpenuhi                                                                          | NOT_READY   |
| GR006 | RC05 tidak terpenuhi                                                                          | NOT_READY   |

---

# 6. Recommendation Matrix

| Criteria | Recommendation                                                           |
| -------- | ------------------------------------------------------------------------ |
| RC01     | Lengkapi seluruh dokumen perizinan.                                      |
| RC02     | Pastikan venue memenuhi kapasitas dan memiliki jalur evakuasi.           |
| RC03     | Lengkapi struktur organisasi dan pembagian tugas panitia.                |
| RC04     | Lengkapi sistem keamanan, APAR, dan prosedur evakuasi.                   |
| RC05     | Sediakan tim medis, ambulans, dan perlengkapan P3K.                      |
| RC06     | Lengkapi logistik utama dan sumber listrik cadangan.                     |
| RC07     | Finalisasi SOP, rundown, dan kesiapan operasional.                       |
| RC08     | Tingkatkan komunikasi internal dan penyampaian informasi kepada peserta. |

---

# 7. Knowledge Coverage

| Component       | Total |
| --------------- | ----: |
| Categories      |     8 |
| Facts           |    40 |
| Category Rules  |     8 |
| Criteria        |     8 |
| Global Rules    |     6 |
| Decisions       |     3 |
| Recommendations |     8 |

---

# 8. Knowledge Flow

```text
User Assessment
        │
        ▼
Answered Facts (F001–F040)
        │
        ▼
Category Rules (CR001–CR008)
        │
        ▼
Criteria (RC01–RC08)
        │
        ▼
Global Rules (GR001–GR006)
        │
        ▼
Decision
        │
        ▼
Recommendations
```

---

# Document Status

| Item         | Value                |
| ------------ | -------------------- |
| Version      | ESKS v1.0            |
| Method       | Forward Chaining     |
| Status       | Approved             |
| Repository   | Knowledge Repository |
| Last Updated | 27 June 2026         |
