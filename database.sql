-- =============================================
-- SIAKAD - Sistem Informasi Akademik
-- Database untuk Aplikasi Desktop Tkinter
-- Nama Database: siakad
-- Dibuat oleh: [Roja] - Semester 4
-- =============================================


DROP DATABASE IF EXISTS siakad;
CREATE DATABASE siakad;
USE siakad;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Operator', 'Mahasiswa') NOT NULL
);

CREATE TABLE mahasiswa (
    nim VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    prodi VARCHAR(100) NOT NULL
);

CREATE TABLE dosen (
    nidn VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    prodi VARCHAR(100) NOT NULL
);

CREATE TABLE matakuliah (
    kode_mk VARCHAR(20) PRIMARY KEY,
    nama_mk VARCHAR(150) NOT NULL,
    sks INT NOT NULL
);

CREATE TABLE m_program_studi (
    id_prodi INT AUTO_INCREMENT PRIMARY KEY,
    kode_prodi VARCHAR(10) UNIQUE NOT NULL,
    nama_prodi VARCHAR(100) NOT NULL,
    jenjang_pendidikan VARCHAR(50) NOT NULL
);

-- Data dummy
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'Admin'),
('operator', 'op123', 'Operator'),
('mhs', 'mhs123', 'Mahasiswa');