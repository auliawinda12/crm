# Panduan Penggunaan Sistem CRM Frappe

## Daftar Isi

1. [Pengenalan](#pengenalan)
2. [Tahap 1: Login ke Sistem](#tahap-1-login-ke-sistem)
3. [Tahap 2: Mengenal Navigasi Utama](#tahap-2-mengenal-navigasi-utama)
4. [Tahap 3: Dashboard](#tahap-3-dashboard)
5. [Tahap 4: Manajemen Leads](#tahap-4-manajemen-leads)
6. [Tahap 5: Manajemen Deals](#tahap-5-manajemen-deals)
7. [Tahap 6: Manajemen Kontak](#tahap-6-manajemen-kontak)
8. [Tahap 7: Manajemen Organisasi](#tahap-7-manajemen-organisasi)
9. [Tahap 8: Tugas (Tasks)](#tahap-8-tugas-tasks)
10. [Tahap 9: Catatan (Notes)](#tahap-9-catatan-notes)
11. [Tahap 10: Kalender](#tahap-10-kalender)
12. [Tahap 11: Log Panggilan (Call Logs)](#tahap-11-log-panggilan-call-logs)
13. [Tahap 12: Impor Data](#tahap-12-impor-data)
14. [Tahap 13: Integrasi](#tahap-13-integrasi)
15. [Tips Penggunaan Efektif](#tips-penggunaan-efektif)

---

## Pengenalan

**Frappe CRM** adalah sistem manajemen hubungan pelanggan (Customer Relationship Management) yang sederhana, terjangkau, dan open-source. Sistem ini dirancang khusus untuk tim penjualan modern dengan pengguna yang tidak terbatas.

### Fitur Utama

- **Ramah Pengguna dan Fleksibel:** Antarmuka yang sederhana, intuitif, dan mudah dinavigasi
- **Halaman Lead/Deal All-in-One:** Menggabungkan semua tindakan dan detail penting dalam satu halaman
- **Tampilan Kanban:** Kelola leads dan deals secara visual dengan papan Kanban drag-and-drop
- **Tampilan Kustom:** Desain tampilan yang dipersonalisasi dengan filter, pengurutan, dan kolom kustom
- **Responsif:** Mendukung tampilan mobile (smartphone) dan desktop

---

## Tahap 1: Login ke Sistem

### 1.1 Persyaratan Sebelum Login

Sebelum memulai, pastikan Anda memiliki:
- **Browser web modern** yang ter-update (Google Chrome, Mozilla Firefox, Microsoft Edge, atau Safari)
- **Koneksi internet** yang stabil
- **Kredensial akun** (username/email dan password) yang diberikan oleh administrator sistem

### 1.2 Langkah-langkah Login

1. **Buka Browser Web**
   - Buka browser web pilihan Anda (disarankan: Google Chrome atau Firefox versi terbaru)

2. **Masukkan URL Sistem**
   - Ketik alamat URL CRM di address bar browser Anda
   - Contoh: `https://crm.perusahaananda.com`
   - Tekan **Enter** pada keyboard

3. **Halaman Login**
   - Anda akan diarahkan ke halaman login Frappe
   - Halaman ini menampilkan formulir login dengan kolom:
     - **Email Address** — Masukkan alamat email yang terdaftar sebagai akun CRM Anda
     - **Password** — Masukkan password Anda

4. **Masukkan Kredensial**
   - Ketik **email** Anda di kolom "Email Address"
   - Ketik **password** Anda di kolom "Password"
   - Pastikan tidak ada spasi tambahan sebelum atau sesudah email/password

5. **Klik Tombol Login**
   - Klik tombol **Login** untuk masuk ke sistem
   - Tunggu beberapa saat hingga sistem memproses autentikasi

6. **Login dengan Akun Sosial (Opsional)**
   - Jika administrator telah mengaktifkan login sosial (misalnya Google, GitHub, dll), Anda akan melihat tombol tambahan di bawah formulir login
   - Klik ikon penyedia layanan yang diinginkan (contoh: **Login with Google**)
   - Anda akan diarahkan ke halaman autentikasi penyedia tersebut
   - Ikuti instruksi untuk memberikan izin akses

### 1.3 Setelah Login Berhasil

Setelah login berhasil, sistem akan mengarahkan Anda ke salah satu halaman berikut:

- **Halaman Welcome** (jika Anda pengguna baru dan belum memiliki data)
  - Di halaman ini Anda dapat:
    - Menambahkan **sample data** (10 leads contoh) untuk mencoba sistem
    - Menghubungkan **email** Anda (sinkronisasi kontak, email, dan kalender via Google)
    - Membuat **lead secara manual** dengan klik "Or create leads manually"

- **Halaman Leads** atau **Dashboard** (jika Anda sudah memiliki data atau tampilan default telah dikonfigurasi)

### 1.4 Mengatasi Masalah Login

| Masalah | Solusi |
|---------|--------|
| Lupa password | Klik link **Forgot Password** di halaman login, masukkan email, dan ikuti instruksi reset password yang dikirim ke email Anda |
| Email tidak terdaftar | Hubungi administrator sistem untuk membuatkan akun baru |
| Halaman "Not Permitted" muncul | Akun Anda belum memiliki akses CRM. Hubungi administrator untuk mendapatkan role/izin CRM |
| Halaman tidak dapat dimuat | Periksa koneksi internet Anda dan pastikan URL sudah benar |

---

## Tahap 2: Mengenal Navigasi Utama

### 2.1 Sidebar (Menu Sisi Kiri)

Setelah login, Anda akan melihat **sidebar** di sisi kiri layar. Sidebar ini berisi menu navigasi utama:

| Ikon/Menu | Fungsi |
|-----------|--------|
| **Dashboard** | Halaman ringkasan statistik dan kinerja |
| **Leads** | Daftar prospek/calon pelanggan |
| **Deals** | Daftar peluang penjualan |
| **Contacts** | Daftar kontak individu |
| **Organizations** | Daftar perusahaan/organisasi |
| **Notes** | Catatan-catatan penting |
| **Tasks** | Daftar tugas yang harus dikerjakan |
| **Call Logs** | Riwayat panggilan telepon |
| **Calendar** | Jadwal dan kalender aktivitas |
| **Data Import** | Fitur impor data massal |

### 2.2 Notifikasi

- Ikon **lonceng (bell)** di pojok kanan atas menampilkan notifikasi terbaru
- Klik ikon tersebut untuk melihat daftar notifikasi
- Notifikasi mencakup: tugas baru, perubahan deal, komentar, dan lainnya

### 2.3 Profil Pengguna

- Klik **avatar/foto profil** Anda di sidebar untuk mengakses:
  - Pengaturan profil
  - Logout dari sistem

---

## Tahap 3: Dashboard

### 3.1 Ringkasan

Dashboard adalah halaman utama yang memberikan gambaran lengkap tentang aktivitas penjualan dan kinerja tim.

### 3.2 Fitur Dashboard

1. **Statistik Ringkas**
   - Jumlah total leads
   - Jumlah total deals
   - Nilai total deals
   - Leads yang dikonversi
   - Win rate (tingkat kemenangan)

2. **Aktivitas Terbaru**
   - Leads baru yang ditambahkan
   - Perubahan status deals
   - Tugas yang baru ditambahkan
   - Catatan yang baru dibuat

3. **Filter Periode**
   - Pilih rentang waktu: Last 7 Days, Last 30 Days, Last 60 Days, Last 90 Days
   - Atau gunakan **Custom Range** untuk memilih tanggal spesifik

4. **Filter Pengguna** (khusus Admin/Manager)
   - Pilih sales user tertentu untuk melihat kinerja individu

### 3.3 Cara Menggunakan Dashboard

1. Klik menu **Dashboard** di sidebar
2. Pilih periode waktu yang diinginkan menggunakan dropdown di bagian atas
3. Tinjau grafik dan statistik yang ditampilkan
4. Admin dapat klik **Edit** untuk menyesuaikan tata letak dashboard
5. Klik **Refresh** untuk memperbarui data

---

## Tahap 4: Manajemen Leads

### 4.1 Apa itu Lead?

Lead adalah calon pelanggan atau prospek yang belum menjadi customer namun memiliki potensi untuk menjadi pembeli.

### 4.2 Melihat Daftar Leads

1. Klik menu **Leads** di sidebar
2. Pilih tampilan yang diinginkan:
   - **List View** — Format tabel dengan kolom yang dapat disesuaikan
   - **Kanban View** — Papan visual berdasarkan status (drag-and-drop)
   - **Group By View** — Pengelompokan berdasarkan kriteria tertentu

### 4.3 Membuat Lead Baru

1. Klik tombol **+ New Lead** di pojok kanan atas
2. Isi formulir:
   - **Nama Lead** (wajib)
   - **Organisasi** (opsional)
   - **Email** (opsional)
   - **Nomor Telepon** (opsional)
   - **Status Lead** (default: New)
   - **Sumber Lead** — Pilih dari: Email, Telepon, Website, Referensi, dll
   - **Keterangan** (opsional)
3. Klik **Save** untuk menyimpan

### 4.4 Mengelola Lead

Klik pada lead dari daftar untuk membuka halaman detail. Di halaman ini Anda dapat:

1. **Tab Activity** — Lihat dan tambah aktivitas:
   - Catatan (Notes)
   - Tugas (Tasks)
   - Panggilan (Calls)
   - Email

2. **Informasi Detail**
   - Informasi kontak
   - Detail organisasi
   - Status dan sumber lead

3. **Ubah Status** — Klik tombol status dan pilih dari dropdown:
   - **New** — Lead baru, belum dihubungi
   - **Contacted** — Sudah dihubungi
   - **Qualified** — Memenuhi kriteria
   - **Unqualified** — Tidak memenuhi kriteria
   - **Converted** — Telah dikonversi menjadi Deal
   - **Lost** — Tidak dilanjutkan

4. **Konversi ke Deal**
   - Klik tombol **Convert to Deal**
   - Isi informasi deal yang akan dibuat
   - Lead akan ditandai sebagai "Converted"

### 4.5 Mengubah Status via Kanban

1. Buka tampilan **Kanban**
2. **Drag-and-drop** kartu lead ke kolom status yang diinginkan
3. Status akan otomatis ter-update

### 4.6 Sample New Template Email untuk Lead (Bahasa Indonesia)

Gunakan contoh berikut saat membuat email template baru:

1. Buka **Settings > Email Templates**
2. Klik **New template**
3. Isi field berikut:
   - **Name:** `Follow Up Lead - ID`
   - **For:** `Lead`
   - **Subject:** `Terima kasih sudah menghubungi kami, {{ lead_name }}`
   - **Content type:** `Rich Text` atau `HTML`

**Contoh konten (Rich Text):**

```text
Halo {{ lead_name }},

Terima kasih sudah menghubungi tim kami.
Kami sudah menerima kebutuhan Anda dan siap membantu proses selanjutnya.

Jika berkenan, balas email ini agar kami bisa menjadwalkan diskusi singkat.

Salam,
Tim Sales
```

**Contoh konten (HTML):**

```html
<p>Halo {{ lead_name }},</p>

<p>Terima kasih sudah menghubungi tim kami.</p>
<p>Kami sudah menerima kebutuhan Anda dan siap membantu proses selanjutnya.</p>

<p>Jika berkenan, balas email ini agar kami bisa menjadwalkan diskusi singkat.</p>

<p>Salam,<br>Tim Sales</p>
```

---

## Tahap 5: Manajemen Deals

### 5.1 Apa itu Deal?

Deal adalah peluang penjualan yang sedang dalam proses negosiasi. Deals umumnya berasal dari leads yang telah dikonversi.

### 5.2 Melihat Daftar Deals

1. Klik menu **Deals** di sidebar
2. Tampilan tersedia: **List**, **Kanban** (berdasarkan tahapan), atau **Group By**

### 5.3 Membuat Deal Baru

1. Klik tombol **+ New Deal**
2. Isi formulir:
   - **Nama Deal** (wajib)
   - **Organisasi** (opsional)
   - **Kontak** (opsional)
   - **Nilai Deal** (angka)
   - **Probabilitas** (persentase)
   - **Tahapan Deal** (default: Prospecting)
   - **Perkiraan Tanggal Penutupan** (opsional)
3. Klik **Save**

### 5.4 Mengelola Deal

Buka detail deal untuk:

1. **Lihat Informasi** — Detail deal, kontak, dan organisasi terkait
2. **Kelola Tahapan** — Pindahkan deal ke tahapan berikutnya, update probabilitas
3. **Tambah Aktivitas** — Catatan, Tugas, Panggilan, Email
4. **Tutup Deal:**
   - Klik **Close as Won** jika deal berhasil
   - Klik **Close as Lost** jika deal gagal

### 5.5 Tahapan Deal Standar

| # | Tahapan | Deskripsi |
|---|---------|-----------|
| 1 | **Prospecting** | Mengidentifikasi prospek |
| 2 | **Qualification** | Memverifikasi kualifikasi |
| 3 | **Proposal** | Mengirim proposal |
| 4 | **Negotiation** | Negosiasi harga dan syarat |
| 5 | **Won** | Deal berhasil ditutup |
| 6 | **Lost** | Deal gagal |

---

## Tahap 6: Manajemen Kontak

### 6.1 Apa itu Kontak?

Kontak adalah orang-orang yang terkait dengan bisnis Anda, termasuk pelanggan, prospek, dan karyawan organisasi klien.

### 6.2 Melihat Daftar Kontak

1. Klik menu **Contacts** di sidebar
2. Lihat semua kontak dalam sistem

### 6.3 Membuat Kontak Baru

1. Klik tombol **+ New Contact**
2. Isi informasi:
   - **Nama Depan** (wajib)
   - **Nama Belakang** (wajib)
   - **Email** (opsional)
   - **Nomor Telepon** (opsional)
   - **Organisasi** (opsional)
   - **Peran/Posisi** (opsional)
   - **Alamat** (opsional)
3. Klik **Save**

### 6.4 Mengelola Kontak

1. Buka detail kontak dengan mengklik nama kontak
2. Anda dapat:
   - Edit informasi kontak
   - Lihat deals dan leads terkait
   - Tambah catatan dan tugas
   - Lihat riwayat aktivitas

### 6.5 Mencari Kontak

- Gunakan kolom **pencarian** di bagian atas daftar
- Ketik nama, email, atau nomor telepon
- Hasil akan muncul secara real-time

---

## Tahap 7: Manajemen Organisasi

### 7.1 Apa itu Organisasi?

Organisasi adalah perusahaan atau entitas bisnis yang terkait dengan leads, deals, dan kontak.

### 7.2 Melihat Daftar Organisasi

1. Klik menu **Organizations** di sidebar
2. Lihat semua organisasi yang terdaftar

### 7.3 Membuat Organisasi Baru

1. Klik tombol **+ New Organization**
2. Isi informasi:
   - **Nama Organisasi** (wajib)
   - **Website** (opsional)
   - **Industri** (opsional)
   - **Alamat** (opsional)
   - **Negara** (opsional)
3. Klik **Save**

### 7.4 Mengelola Organisasi

1. Klik pada organisasi untuk membuka detail
2. Anda dapat:
   - Melihat kontak-kontak dari organisasi tersebut
   - Melihat leads dan deals terkait
   - Edit informasi organisasi
   - Tambah catatan

---

## Tahap 8: Tugas (Tasks)

### 8.1 Apa itu Tugas?

Tugas adalah aktivitas yang perlu diselesaikan terkait dengan leads, deals, atau kontak.

### 8.2 Melihat Daftar Tugas

1. Klik menu **Tasks** di sidebar
2. Lihat semua tugas yang ditugaskan kepada Anda

### 8.3 Membuat Tugas Baru

**Dari Menu Tasks:**
1. Klik tombol **+ New Task**
2. Isi informasi:
   - **Judul Tugas** (wajib)
   - **Deskripsi** (opsional)
   - **Tanggal Tenggat** (wajib)
   - **Prioritas** — Low, Medium, High, atau Urgent
   - **Status** — Open, In Progress, Completed, atau Cancelled
   - **Tetapkan kepada** (opsional)
   - **Tautkan ke Lead/Deal/Kontak** (opsional)
3. Klik **Save**

**Dari Halaman Detail Lead/Deal/Kontak:**
1. Buka detail Lead/Deal/Kontak
2. Klik tab **Activities**
3. Klik tombol **+ Task**
4. Isi informasi tugas
5. Klik **Save**

### 8.4 Mengelola Tugas

1. Klik pada tugas untuk membuka detail
2. Anda dapat: edit tugas, ubah status, tambah komentar, atau tandai sebagai selesai

### 8.5 Status Tugas

| Status | Keterangan |
|--------|------------|
| **Open** | Tugas baru, belum dikerjakan |
| **In Progress** | Tugas sedang dikerjakan |
| **Completed** | Tugas telah selesai |
| **Cancelled** | Tugas dibatalkan |

---

## Tahap 9: Catatan (Notes)

### 9.1 Apa itu Catatan?

Catatan adalah informasi penting atau memo yang ingin Anda simpan terkait leads, deals, atau kontak.

### 9.2 Membuat Catatan

**Dari Menu Notes:**
1. Klik menu **Notes** di sidebar
2. Klik tombol **+ New Note**
3. Isi judul dan isi catatan
4. Tautkan ke Lead/Deal/Kontak (opsional)
5. Klik **Save**

**Dari Halaman Detail:**
1. Buka detail Lead/Deal/Kontak
2. Klik tab **Activities**
3. Klik tombol **+ Note**
4. Tulis catatan, lalu klik **Save**

### 9.3 Mengelola Catatan

- Klik pada catatan untuk melihat detail
- Edit atau hapus catatan sesuai kebutuhan
- Lihat item terkait dengan catatan tersebut

---

## Tahap 10: Kalender

### 10.1 Ringkasan

Kalender membantu Anda mengatur jadwal aktivitas, tugas, dan pertemuan.

### 10.2 Menggunakan Kalender

1. Klik menu **Calendar** di sidebar
2. Anda akan melihat tampilan kalender

### 10.3 Navigasi Kalender

- **Panah kiri/kanan** — Berpindah antar bulan
- **Tombol "Today"** — Kembali ke bulan/minggu saat ini
- **Dropdown** — Pilih bulan/tahun spesifik

### 10.4 Melihat Aktivitas

- Aktivitas dengan tanggal tenggat ditampilkan pada kalender
- Klik pada tanggal untuk melihat detail aktivitas hari tersebut
- Warna berbeda menandakan jenis aktivitas yang berbeda

---

## Tahap 11: Log Panggilan (Call Logs)

### 11.1 Ringkasan

Log Panggilan mencatat semua panggilan yang dilakukan dan diterima melalui sistem CRM (memerlukan integrasi dengan Twilio atau Exotel).

### 11.2 Melihat Log Panggilan

1. Klik menu **Call Logs** di sidebar
2. Lihat daftar semua panggilan

### 11.3 Informasi Log Panggilan

Setiap log panggilan menampilkan:

| Kolom | Deskripsi |
|-------|-----------|
| **Tanggal/Waktu** | Kapan panggilan terjadi |
| **Nomor** | Nomor yang dihubungi/menelepon |
| **Durasi** | Lama panggilan |
| **Status** | Connected, Missed, dll |
| **Arahan** | Incoming atau Outgoing |
| **Recording** | Link ke rekaman (jika tersedia) |
| **Catatan** | Catatan tentang panggilan |

### 11.4 Menambah Catatan Panggilan

1. Klik pada log panggilan
2. Klik **Add Note**
3. Tulis catatan, lalu klik **Save**

---

## Tahap 12: Impor Data

### 12.1 Ringkasan

Fitur Data Import memungkinkan Anda mengimpor leads, kontak, organisasi, dan deals dari file CSV atau Excel dalam jumlah banyak.

### 12.2 Langkah-langkah Impor

1. Klik menu **Data Import** di sidebar
2. Pilih jenis data: Leads, Contacts, Organizations, atau Deals
3. Klik **Upload File** dan pilih file CSV/Excel
4. **Review mapping kolom:**
   - Sesuaikan kolom file dengan kolom sistem
   - Pastikan kolom wajib terisi
5. Klik **Start Import**

### 12.3 Format File yang Didukung

- **CSV** (Comma Separated Values)
- **Excel** (.xlsx, .xls)

### 12.4 Tips Impor Data

- Pastikan file memiliki header yang jelas
- Hapus baris kosong dari file
- Pastikan format email valid
- Kolom wajib per jenis data:

| Jenis Data | Kolom Wajib |
|------------|-------------|
| Leads | Nama Lead |
| Contacts | Nama Depan, Nama Belakang |
| Organizations | Nama Organisasi |
| Deals | Nama Deal |

### 12.5 Review Hasil Impor

Setelah impor selesai:
- Cek jumlah baris yang berhasil diimpor
- Periksa baris yang gagal dan alasan kegagalan
- Review data yang diimpor untuk memastikan kebenaran

---

## Tahap 13: Integrasi

### 13.1 WhatsApp

- **Deskripsi:** Kirim dan terima pesan WhatsApp langsung dari CRM
- **Penggunaan:**
  1. Buka detail Lead/Deal/Kontak
  2. Klik tombol **WhatsApp**
  3. Tulis pesan dan kirim
- **Setup:** Memerlukan integrasi dengan Frappe WhatsApp

### 13.2 Twilio (Telepon)

- **Deskripsi:** Membuat dan menerima panggilan telepon dengan rekaman
- **Penggunaan:** Panggilan langsung dari detail kontak, semua tercatat di Call Logs

### 13.3 Exotel (Telepon)

- **Deskripsi:** Membuat dan menerima panggilan melalui telepon agen
- **Penggunaan:** Mirip dengan Twilio, menggunakan telepon seluler agen

### 13.4 ERPNext

- **Deskripsi:** Integrasi dengan ERPNext untuk fitur tambahan
- **Fitur:** Invoice penjualan, Akuntansi, Inventaris, Purchasing

> **Catatan:** Hubungi administrator sistem untuk mengaktifkan dan mengkonfigurasi integrasi.

---

## Tips Penggunaan Efektif

### Organisasi Data
- Gunakan **Custom Views** untuk membuat filter yang sering digunakan
- Beri nama tampilan yang deskriptif
- Bagikan tampilan kustom dengan tim

### Manajemen Leads
- Update status lead secara rutin
- Tambahkan catatan setelah setiap interaksi
- Konversi lead ke deal secepat mungkin jika potensial

### Manajemen Deals
- Update probabilitas secara berkala
- Gunakan Kanban View untuk melihat progres deals
- Tetapkan tanggal penutupan yang realistis

### Manajemen Waktu
- Gunakan Tugas untuk semua follow-up yang diperlukan
- Set reminder untuk tugas penting
- Periksa kalender setiap pagi

### Kolaborasi Tim
- Tetapkan tugas kepada anggota tim yang tepat
- Gunakan komentar untuk berdiskusi dalam sistem
- Share notes penting dengan tim

### Kualitas Data
- Selalu lengkapi informasi kontak
- Perbarui informasi yang sudah berubah
- Hapus atau tandai data yang tidak relevan

---

## Glossarium

| Istilah | Definisi |
|---------|----------|
| **CRM** | Customer Relationship Management — Manajemen Hubungan Pelanggan |
| **Lead** | Prospek atau calon pelanggan |
| **Deal** | Peluang penjualan yang sedang dinegosiasi |
| **Kanban** | Metode visual manajemen dengan papan drag-and-drop |
| **Pipeline** | Tahapan alur dari lead sampai menjadi pelanggan |
| **Conversion Rate** | Persentase leads yang dikonversi menjadi deals/pelanggan |
| **Win Rate** | Persentase deals yang berhasil ditutup |
| **Probability** | Perkiraan peluang keberhasilan sebuah deal |

---

## Dukungan dan Bantuan

### Dokumentasi Lengkap
- [Dokumentasi Resmi Frappe CRM](https://docs.frappe.io/crm)

### Komunitas
- [Grup Telegram](https://t.me/frappecrm)
- [Forum Diskusi](https://discuss.frappe.io/c/frappe-crm)
- [YouTube](https://www.youtube.com/channel/UCn3bV5kx77HsVwtnlCeEi_A)
- [Twitter/X](https://x.com/frappetech)

### Bantuan Administrator
Hubungi administrator sistem jika mengalami masalah dengan: login, error teknis, permintaan fitur baru, atau integrasi.

---

**Versi Dokumen:** 2.0  
**Terakhir Diperbarui:** Februari 2026  
**Produk:** Frappe CRM


grqh ayqv thrs ctii
