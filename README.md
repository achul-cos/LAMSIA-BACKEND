<div align="center">

# 💊 LAMSIA — Backend API

**LAMSIA** (*Layanan Manajemen Smart Medication Box IoT*) adalah sistem backend untuk kotak obat pintar berbasis IoT yang membantu pengguna mengelola jadwal dan konsumsi obat secara otomatis.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Tech Stack](#-tech-stack)
- [Struktur Proyek](#-struktur-proyek)
- [Prasyarat](#-prasyarat)
- [Instalasi & Konfigurasi](#-instalasi--konfigurasi)
- [Menjalankan Server](#-menjalankan-server)
- [Migrasi Database](#-migrasi-database)
- [Troubleshooting](#-troubleshooting)

---

## 📖 Tentang Proyek

LAMSIA-BACKEND adalah REST API berbasis **FastAPI** yang menjadi jembatan komunikasi antara perangkat keras IoT (Arduino / Raspberry Pi) dan aplikasi klien. Sistem ini mengelola data pengguna, jadwal konsumsi obat, dan status kotak obat secara real-time melalui protokol MQTT dan HTTP.

---

## 🛠 Tech Stack

| Komponen | Teknologi |
|---|---|
| Framework API | FastAPI + Uvicorn |
| ORM / Database | SQLAlchemy + PyMySQL |
| Database | MySQL 8.0 |
| Konfigurasi Env | python-dotenv |
| Utilities | inflect, faker |

---

## 📁 Struktur Proyek

```
LAMSIA-BACKEND/
├── app/                  # Kode utama aplikasi FastAPI
├── cli/                  # CLI tools (seed data, utilitas)
├── tests/                # Unit & integration tests
├── create_tables.py      # Script migrasi database
├── lamsia.py             # Entry point alternatif
├── requirements.txt      # Daftar dependensi Python
├── .env.example          # Template konfigurasi environment
└── README.md
```

---

## ✅ Prasyarat

Pastikan sudah terinstall di sistem kamu:

- **Python** `3.10+` — [download](https://www.python.org/downloads/)
- **MySQL Server** `8.0+` — [download](https://dev.mysql.com/downloads/mysql/)
- **Git** — [download](https://git-scm.com/)

---

## ⚙️ Instalasi & Konfigurasi

### 1. Clone Repositori

```bash
git clone https://github.com/achul-cos/LAMSIA-BACKEND.git
cd LAMSIA-BACKEND
```

### 2. Konfigurasi Environment

Duplikat file `.env.example` dan rename menjadi `.env`:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Kemudian isi variabel berikut di `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=lamsia_db
```

### 3. Siapkan Database MySQL

Buka terminal MySQL dan buat database baru:

```bash
# Masuk ke MySQL
mysql -u root -p

# Atau jika perlu path lengkap (Windows)
# "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

```sql
-- Buat database
CREATE DATABASE lamsia_db;

-- Verifikasi
SHOW DATABASES;
```

Output yang diharapkan:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| lamsia_db          |  ✓
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

### 4. Setup Virtual Environment

```bash
# Buat venv
python -m venv venv

# Aktivasi (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Aktivasi (macOS / Linux)
source venv/bin/activate
```

> **Catatan:** Jika muncul error aktivasi di Windows, lihat bagian [Troubleshooting](#-troubleshooting).

### 5. Install Dependensi

```bash
pip install -r requirements.txt
```

---

## 🚀 Menjalankan Server

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Dokumentasi API otomatis tersedia di:
- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Untuk keluar dari virtual environment:

```bash
deactivate
```

---

## 🗄 Migrasi Database

Tabel database dibuat otomatis saat server pertama kali dijalankan melalui `create_tables.py`. Untuk memverifikasi hasilnya secara manual:

```sql
USE lamsia_db;

-- Cek tabel yang tersedia
SHOW TABLES;

-- Cek struktur tabel users
DESCRIBE users;
```

Output yang diharapkan untuk `DESCRIBE users`:

```
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int          | NO   | PRI | NULL    | auto_increment |
| username  | varchar(100) | NO   |     | NULL    |                |
| telephone | varchar(100) | NO   |     | NULL    |                |
| password  | varchar(255) | NO   |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
```

---

## 🔧 Troubleshooting

### Error: Script tidak bisa dijalankan di PowerShell

Jika muncul error berikut saat aktivasi venv:

```
.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Solusi 1** — Ubah execution policy untuk user saat ini (disarankan):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solusi 2** — Bypass untuk sesi ini saja (jika tidak punya hak admin):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Solusi 3** — Jalankan Python langsung via path venv (tanpa aktivasi):

```powershell
# Cek versi
.\venv\Scripts\python.exe --version

# Lihat package terinstall
.\venv\Scripts\python.exe -m pip list

# Jalankan server
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

---

<div align="center">

Dibuat dengan ❤️ oleh [Nasrullah (Achul)](https://github.com/achul-cos) dan [Steven](https://github.com/Stevv07)

</div>