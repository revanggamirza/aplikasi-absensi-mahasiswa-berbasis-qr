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
<img width="1841" height="1034" alt="image" src="https://github.com/user-attachments/assets/36cb1c5e-b426-4710-b424-ab246a56936a" />
<img width="1909" height="1196" alt="image" src="https://github.com/user-attachments/assets/eba4cf65-6101-40e6-87a6-b019fecc1393" />


### 👨‍🎓 Manajemen Mahasiswa
- Tambah data mahasiswa (NPM, Nama, Kelas)
- Generate QR Code unik berdasarkan NPM
- Download QR Code dalam format PNG
- Daftar mahasiswa tersimpan di database SQLite
<img width="1904" height="1195" alt="image" src="https://github.com/user-attachments/assets/5261d723-a66d-4615-8197-dd5682fb1846" />
<img width="1919" height="1112" alt="image" src="https://github.com/user-attachments/assets/d99b7503-bd79-4b29-a5f5-ed4d13fd67a4" />



### 📷 Scan Absensi QR Code
- Scan QR Code secara **real-time menggunakan kamera**
- Deteksi QR menggunakan **OpenCV**
- Pencegahan absensi ganda (sekali per hari)
- Validasi NPM terdaftar
- Status scan ditampilkan langsung
<img width="1919" height="1199" alt="image" src="https://github.com/user-attachments/assets/422e8b9d-363d-40c8-9da7-92c87e5266c0" />
<img width="1918" height="1199" alt="image" src="https://github.com/user-attachments/assets/52fa7aed-7ffa-4b33-8aa9-ea75aa06fac5" />
<img width="1919" height="1196" alt="image" src="https://github.com/user-attachments/assets/0e94c342-7a73-475c-bf4d-84463cfb9331" />



### 📊 Dashboard
- Menampilkan:
  - Hari & tanggal saat ini
  - Total mahasiswa
  - Jumlah absensi IN & OUT hari ini
  - Grafik absensi
  - Aktivitas absensi terakhir
<img width="1916" height="1164" alt="image" src="https://github.com/user-attachments/assets/1b203efe-a048-48c9-a2bf-453d9d6e410d" />


### 📋 Rekap Absensi
- Menampilkan data absensi dalam bentuk tabel
- Data diambil langsung dari database
<img width="1919" height="1118" alt="image" src="https://github.com/user-attachments/assets/c54e1548-adb2-4623-adb7-599dd19146e6" />

---

## 🧱 Struktur Folder Project
<img width="995" height="695" alt="image" src="https://github.com/user-attachments/assets/fc72e311-98e9-4688-ba4d-87d6b38909c4" />
<img width="914" height="1556" alt="absensi Diagram drawio" src="https://github.com/user-attachments/assets/7a85ffd4-8230-4bfe-85b3-16d48cb0b3db" />




