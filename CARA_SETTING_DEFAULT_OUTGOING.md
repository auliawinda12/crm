# CARA SETTING DEFAULT OUTGOING EMAIL ACCOUNT
## Panduan Langkah demi Langkah via UI CRM

---

## LANGKAH 1: Buka Email Account

1. **Login ke CRM** sebagai Administrator
2. Di menu sidebar, klik **Settings** (ikon gear)
3. Pilih menu **Emails** atau **Email Account**

---

## LANGKAH 2: Edit Email Account ceklan62@gmail.com

1. Cari email account **ceklan62@gmail.com** dalam daftar
2. Klik tombol **Edit** (ikon pensil) pada baris ceklan62@gmail.com

---

## LANGKAH 3: Checklist Setting Penting

Di form edit Email Account, pastikan/checklist:

### ✅ Enable Outgoing
- Cari field **Enable Outgoing** atau **Enable Sending**
- Pastikan statusnya **Checked** / **Yes** / **1**
- Jika belum, **centang/checklist** checkbox ini

### ✅ Default Outgoing  
- Cari field **Default Outgoing** atau **Default Outgoing Email**
- Pastikan statusnya **Checked** / **Yes** / **1**
- Jika belum, **centang/checklist** checkbox ini ⭐ **INI YANG PALING PENTING!**

---

## LANGKAH 4: Uncheck Default Outgoing Email Lain (Jika Ada)

Jika ada email account lain yang juga tercentang "Default Outgoing":

1. Simpan dulu perubahan ceklan62@gmail.com
2. Kembali ke daftar Email Account
3. Edit email account lain tersebut
4. **Uncheck/Uncentang** field "Default Outgoing"
5. Simpan

⚠️ **PASTIKAN HANYA SATU** email account yang memiliki "Default Outgoing" tercentang, yaitu ceklan62@gmail.com!

---

## LANGKAH 5: Verifikasi

Setelah menyimpan:

1. Kembali ke daftar **Email Account**
2. Lihat kolom/field **Default Outgoing**
3. Pastikan HANYA **ceklan62@gmail.com** yang memiliki tanda centang/check ✅
4. Pastikan ceklan62@gmail.com juga memiliki **Enable Outgoing** tercentang ✅

---

## LANGKAH 6: Restart Container (Opsional tapi Disarankan)

Jika setting sudah benar tapi email masih tidak berubah:

1. Buka terminal/command prompt
2. Jalankan perintah:
   ```bash
   cd C:\Users\62822\Documents\Projects\crm\docker
   docker compose restart
   ```
3. Tunggu sampai restart selesai
4. Buka kembali CRM di browser

---

## VERIFIKASI DATABASE (Opsional - untuk Advanced User)

Jika Anda ingin memverifikasi langsung di database:

### Via MariaDB/MySQL Console:

```sql
USE `crm.localhost`;  -- atau nama database Anda

SELECT 
    name,
    email_id,
    default_outgoing,
    enable_outgoing,
    smtp_server
FROM `tabEmail Account`
ORDER BY email_id;
```

**Hasil yang diharapkan:**
```
+----------------------+-------------------+------------------+------------------+---------------+
| name                | email_id          | default_outgoing  | enable_outgoing  | smtp_server    |
+----------------------+-------------------+------------------+------------------+---------------+
| [nama-account]      | ceklan62@gmail.com| 1                | 1                | smtp.gmail.com  |
+----------------------+-------------------+------------------+------------------+---------------+
```

Pastikan:
- `default_outgoing` = **1** (atau ada check)
- `enable_outgoing` = **1** (atau ada check)

**Untuk mengupdate langsung via SQL:**
```sql
UPDATE `tabEmail Account` 
SET default_outgoing = 1, enable_outgoing = 1
WHERE email_id = 'ceklan62@gmail.com';

UPDATE `tabEmail Account` 
SET default_outgoing = 0
WHERE email_id != 'ceklan62@gmail.com';
```

---

## TROUBLESHOOTING

### Masalah 1: Tidak bisa centang Default Outgoing

**Penyebab**: Ada error validasi atau field readonly

**Solusi**:
1. Pastikan email account **Enable Outgoing** sudah dicentang dulu
2. Simpan, lalu edit lagi
3. Baru centang Default Outgoing
4. Simpan lagi

### Masalah 2: Setelah dicentang, kembali unchecked

**Penyebab**: Ada hook/validator yang mereset

**Solusi**:
1. Cek log error di browser console (F12)
2. Atau cek log container: `docker compose logs frappe --tail 100`
3. Hubungi developer untuk cek hooks

### Masalah 3: Setting sudah benar tapi sender masih Administrator

**Penyebab**: Container belum me-reload konfigurasi

**Solusi**:
1. **WAJIB** restart container: `docker compose -f docker/docker-compose.yml restart`
2. Clear browser cache (Ctrl + F5)
3. Coba kirim email lagi

### Masalah 4: Email account ceklan62@gmail.com tidak ada di daftar

**Solusi - Buat Baru:**
1. Klik tombol **New** / **Add** / **Create**
2. Isi form:
   - **Email Account Name**: Ceklan62 Gmail
   - **Email ID**: ceklan62@gmail.com
   - **Service**: GMail / Gmail
   - **Enable Incoming**: Yes (opsional)
   - **Enable Outgoing**: **YES (WAJIB)**
   - **Default Outgoing**: **YES (WAJIB)**
   - **Password**: App Password dari Google (16 digit)
3. Klik **Save**
4. Verifikasi SMTP connection akan otomatis dilakukan

---

## APP PASSWORD GMAIL (PENTING!)

Jika password Anda masih password Gmail biasa, **Wajib diganti**:

### Cara Membuat App Password:

1. Buka https://myaccount.google.com/security
2. Cari section **2-Step Verification**
3. Jika belum aktif, **aktifkan dulu**
4. Setelah aktif, buka https://myaccount.google.com/apppasswords
5. Klik **Select app**: pilih **Mail**
6. Klik **Select device**: pilih **Windows Computer** (atau yang lain)
7. Klik **Generate**
8. Copy password 16 digit yang muncul (format: `xxxx xxxx xxxx xxxx`)
9. Gunakan password ini di Email Account CRM

⚠️ **JANGAN GUNAKAN PASSWORD GMAIL BIASA!** Google tidak mengizinkan login pihak ketiga dengan password biasa lagi.

---

## CHECKLIST FINAL

Sebelum mengirim email ke Mr Teuku Audi, pastikan:

- [ ] Email Account ceklan62@gmail.com sudah dibuat
- [ ] **Enable Outgoing**: **CHECKED** ✅
- [ ] **Default Outgoing**: **CHECKED** ✅
- [ ] Tidak ada email account lain yang "Default Outgoing" tercentang
- [ ] Password menggunakan **App Password** Google (16 digit)
- [ ] 2-Step Verification sudah aktif di Google Account
- [ ] SMTP Server: smtp.gmail.com
- [ ] SMTP Port: 587
- [ ] Use TLS: Yes
- [ ] Container sudah di-restart
- [ ] Lead memiliki email address yang valid

---

## TEST PENGIRIMAN EMAIL

Setelah semua setting benar:

1. Buka **CRM > Leads**
2. Cari lead **Mr Teuku Audi**
3. Klik tombol **Reply/Email**
4. Tulis subject dan pesan
5. Klik **Send**
6. Buka tab **Communications** di lead
7. Cek field **From/Sender**
8. Seharusnya sekarang menampilkan: **ceklan62@gmail.com**

Jika masih Administrator:
- Clear cache browser (Ctrl + Shift + Delete)
- Restart container lagi
- Cek kembali setting Default Outgoing

---

**Status Setting:**
```
✅ Default Outgoing: CHECKED (ceklan62@gmail.com)
✅ Enable Outgoing: CHECKED
✅ Siap mengirim email!
```

---

**Dibuat**: 2026-02-12
**File Referensi**:
- `crm/api/communication.py` - API baru yang menggunakan Default Outgoing
- `frontend/src/components/CommunicationArea.vue` - Update API call
