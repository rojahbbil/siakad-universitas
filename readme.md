# SIAKAD - Sistem Informasi Akademik

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Aplikasi desktop **Sistem Informasi Akademik (SIAKAD)** berbasis Python dengan antarmuka Tkinter dan database MySQL. Dilengkapi sistem autentikasi berbasis role.

---

##Fitur

- Sistem Login dengan 3 Role (Admin, Operator, Mahasiswa)
- CRUD Lengkap untuk:
  - Data Mahasiswa
  - Data Dosen
  - Data Mata Kuliah
  - Data Program Studi
- Role-Based Access Control
- Validasi input dan konfirmasi penghapusan
- Tampilan GUI yang clean dan responsif

---

##Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python 3.10+
- **GUI**: Tkinter + ttk
- **Database**: MySQL
- **Connector**: mysql-connector-python

---

## Cara Menjalankan

###1. Persiapan Database
- Buka **XAMPP** → **Laragon**
- Import file `database.sql` yang tersedia di repository

### 2. Install Dependencies
```bash
pip install -r requirements.txt

### 3. Jalankan Aplikasi
python main.py

### Akun Login

Username,Password,Role
admin,admin123,Admin
operator,op123,Operator
mhs,mhs123,Mahasiswa

## 📁 Struktur Folder

siakad-universitas/
├── main.py
├── forms.py
├── database.sql
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    ├── 1-Beranda admin.png
    ├── 2-Managemen Data Mahasiswa.png
    ├── 3-Managemen Data Dosen.png
    ├── 4-Managemen Data Prodi.png
    ├── 5-Managemen Mata Kuliah.png
    └── 6-Operator login.png
    └── 6-Mahasiswa Login.png
    ├── 5-Mahasiswa Fitur.png


### Tujuan Proyek

Proyek ini dibuat untuk memenuhi tugas mata kuliah Pemrograman Desktop Semester 4. Proyek ini membantu saya memahami konsep:

Database Management (MySQL)
GUI Development dengan Tkinter
CRUD Operations
Role-Based Access Control

## 📸 Screenshot Aplikasi

### Login & Beranda
![Beranda Admin](screenshots/1-Beranda admin.png)
![Operator Login](screenshots/6-Operator login.png)
![Mahasiswa Login](screenshots/6-Mahasiswa Login.png)

### Manajemen Data Mahasiswa
![Manajemen Data Mahasiswa](screenshots/2-Managemen Data Mahasiswa.png)
![Mahasiswa Fitur](screenshots/5-Mahasiswa Fitur.png)

### Manajemen Data Dosen
![Manajemen Data Dosen](screenshots/3-Managemen Data Dosen.png)

### Manajemen Data Program Studi
![Manajemen Data Prodi](screenshots/4-Managemen Data Prodi.png)

### Manajemen Mata Kuliah
![Manajemen Mata Kuliah](screenshots/5-Managemen Mata Kuliah.png)

Dibuat oleh: [Roja Hubbil Khairi]
NIM: [24146036]
Semester: 4
Tahun: 2026