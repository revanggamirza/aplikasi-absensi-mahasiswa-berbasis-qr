# 📷 Sistem Absensi Mahasiswa Berbasis QR Code

Aplikasi **Sistem Absensi Mahasiswa berbasis QR Code** menggunakan **Streamlit**, **OpenCV**, dan **SQLite**.  
Aplikasi ini memungkinkan admin melakukan pendataan mahasiswa, generate QR Code, melakukan scan absensi secara real-time melalui kamera, serta melihat rekap dan dashboard absensi.

---

## 🎯 Tujuan Aplikasi
- Menerapkan konsep **sistem informasi absensi digital**
- Mengurangi kecurangan absensi manual
- Mempermudah rekap dan monitoring kehadiran mahasiswa
- Menerapkan konsep **modular programming** dalam Python

---

## 🚀 Fitur Utama

### 🔐 Autentikasi Admin
- Login sederhana menggunakan username & password
- Logout langsung dari sidebar

### 👨‍🎓 Manajemen Mahasiswa
- Tambah data mahasiswa (NPM, Nama, Kelas)
- Generate QR Code unik berdasarkan NPM
- Download QR Code dalam format PNG
- Daftar mahasiswa tersimpan di database SQLite

### 📷 Scan Absensi QR Code
- Scan QR Code secara **real-time menggunakan kamera**
- Deteksi QR menggunakan **OpenCV**
- Pencegahan absensi ganda (sekali per hari)
- Validasi NPM terdaftar
- Status scan ditampilkan langsung

### 📊 Dashboard
- Menampilkan:
  - Hari & tanggal saat ini
  - Total mahasiswa
  - Jumlah absensi IN & OUT hari ini
  - Grafik absensi
  - Aktivitas absensi terakhir

### 📋 Rekap Absensi
- Menampilkan data absensi dalam bentuk tabel
- Data diambil langsung dari database

---

## 🧱 Struktur Folder Project

