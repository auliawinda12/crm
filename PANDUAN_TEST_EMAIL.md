# PANDUAN TEST PENGIRIMAN EMAIL

## Perubahan yang Telah Dibuat:

### 1. Backend API Baru
**File**: `crm/api/communication.py` (baru)

Fungsi: `crm.api.communication.make()`
- Otomatis menggunakan **Default Outgoing Email Account** sebagai sender
- Tidak lagi menggunakan email Administrator

### 2. Frontend Update
**File**: `frontend/src/components/CommunicationArea.vue` (line 203)

Perubahan:
- Mengganti API call dari `frappe.core.doctype.communication.email.make`
- Menjadi `crm.api.communication.make`
- Menghapus hardcoded sender email

---

## LANGKAH TEST PENGIRIMAN EMAIL

### Langkah 1: Verifikasi Konfigurasi Email Account

1. Login ke CRM sebagai Administrator
2. Buka menu **Settings > Emails** atau **Email Account**
3. Cari email account **ceklan62@gmail.com**
4. Klik **Edit** dan pastikan:
   - ✅ **Email ID**: ceklan62@gmail.com
   - ✅ **Enable Outgoing**: Yes/Checked
   - ✅ **Default Outgoing**: Yes/Checked **(INI PENTING!)**
   - ✅ **SMTP Server**: smtp.gmail.com
   - ✅ **SMTP Port**: 587
   - ✅ **Use TLS**: Yes/Checked
   - ✅ **Password**: App Password dari Google (16 digit)

5. Jika ada email account lain yang juga "Default Outgoing", **uncheck** yang lain
6. Simpan (Save)

### Langkah 2: Pastikan App Password Gmail

Jika belum menggunakan App Password:

1. Buka https://myaccount.google.com/security
2. Aktifkan **2-Step Verification** (jika belum)
3. Setelah aktif, buka https://myaccount.google.com/apppasswords
4. Pilih:
   - **Select app**: Mail
   - **Select device**: Windows Computer
5. Klik **Generate**
6. **Copy password 16 digit** yang muncul (format: xxxx xxxx xxxx xxxx)
7. Update Email Account ceklan62@gmail.com dengan password ini

### Langkah 3: Test Pengiriman Email

#### Cara A: Test dari Lead (Recommended)

1. Buka **CRM > Leads**
2. Cari lead **Mr Teuku Audi**
3. Klik untuk membuka detail lead
4. Pastikan lead memiliki email address
5. Klik tombol **Reply/Email** (ikon email)
6. Tulis subject dan pesan test, contoh:
   - **Subject**: Test Email dari CRM
   - **Message**: Hi, ini adalah test email dari sistem CRM kami.
7. Klik **Send**
8. Perhatikan sender email yang muncul di form

#### Cara B: Test Send ke Diri Sendiri

1. Buat lead baru dengan email Anda sendiri
2. Atau edit lead existing dan ganti email dengan email Anda
3. Kirim email test ke lead tersebut
4. Buka inbox email Anda dan cek apakah email diterima
5. Cek sender email apakah dari ceklan62@gmail.com

### Langkah 4: Verifikasi Hasil

#### Cek di CRM:

1. Setelah mengirim, buka tab **Communications** di lead
2. Klik email yang baru dikirim
3. Cek field **From/Sender** - seharusnya: `ceklan62@gmail.com`
4. Cek **Status** - seharusnya: **Sent** atau **Open**

#### Cek di Email Inbox:

1. Buka inbox email penerima (Mr Teuku Audi atau email test Anda)
2. Cari email dari CRM
3. Buka dan cek:
   - **From**: ceklan62@gmail.com
   - **Subject**: sesuai yang Anda kirim
   - **Content**: sesuai yang Anda tulis

---

## TROUBLESHOOTING

### Masalah 1: Sender masih Administrator <admin@example.com>

**Penyebab**: Default Outgoing belum diset dengan benar

**Solusi**:
1. Buka Email Account list
2. Pastikan HANYA SATU yang memiliki **Default Outgoing** checked
3. Email tersebut harus ceklan62@gmail.com
4. Restart container: `docker compose -f docker/docker-compose.yml restart`

### Masalah 2: Email tidak terkirim (Error)

**Penyebab A**: Password Gmail salah atau bukan App Password

**Solusi**:
1. Pastikan menggunakan **App Password** 16 digit, bukan password Gmail biasa
2. Generate ulang App Password di https://myaccount.google.com/apppasswords
3. Update Email Account dengan App Password baru

**Penyebab B**: 2FA belum aktif

**Solusi**:
1. Aktifkan 2-Step Verification di Google Account
2. Baru kemudian generate App Password

**Penyebab C**: Port 587 terblokir

**Solusi**:
1. Cek firewall/network
2. Atau coba gunakan port 465 (SSL) instead of 587 (TLS)

### Masalah 3: Email terkirim tapi tidak diterima

**Penyebab**: Masuk ke Spam/Junk folder

**Solusi**:
1. Cek folder Spam/Junk di inbox penerima
2. Jika ada di spam, mark sebagai "Not Spam"
3. Tambahkan ke Contacts/Address Book

### Masalah 4: API Error

**Penyebab**: File communication.py belum ter-load

**Solusi**:
1. Pastikan container sudah di-restart
2. Cek log: `docker compose -f docker/docker-compose.yml logs frappe --tail 100`
3. Restart lagi jika perlu: `docker compose -f docker/docker-compose.yml restart`

---

## VERIFIKASI KONFIGURASI VIA CONSOLE

Jika ingin memverifikasi via console/terminal:

### Cek Default Outgoing Email Account:

```bash
docker compose -f docker/docker-compose.yml exec frappe sh -c "cd /home/frappe && bench console"
```

Lalu jalankan di console:

```python
import frappe

# Cek default outgoing email account
email_account = frappe.db.get_value(
    "Email Account",
    {"default_outgoing": 1, "enable_outgoing": 1},
    ["name", "email_id", "smtp_server"],
    as_dict=True
)

print("Default Outgoing Email Account:")
print(f"Name: {email_account.get('name') if email_account else 'NOT FOUND'}")
print(f"Email: {email_account.get('email_id') if email_account else 'NOT FOUND'}")
print(f"SMTP: {email_account.get('smtp_server') if email_account else 'NOT FOUND'}")

# Cek semua email accounts
all_accounts = frappe.get_all("Email Account", fields=["name", "email_id", "default_outgoing", "enable_outgoing"])
print("\nSemua Email Accounts:")
for acc in all_accounts:
    print(f"- {acc.get('email_id')} | Default Outgoing: {acc.get('default_outgoing')} | Enable Outgoing: {acc.get('enable_outgoing')}")

exit()
```

---

## CHECKLIST VERIFIKASI

Sebelum mengirim email ke lead Mr Teuku Audi, pastikan:

- [ ] Email Account ceklan62@gmail.com sudah dibuat
- [ ] Default Outgoing sudah di-centang/check
- [ ] Tidak ada email account lain yang juga Default Outgoing
- [ ] Enable Outgoing sudah di-centang
- [ ] Menggunakan App Password dari Google (16 digit)
- [ ] 2-Step Verification sudah aktif di Google Account
- [ ] SMTP Server: smtp.gmail.com
- [ ] SMTP Port: 587
- [ ] Use TLS: Yes
- [ ] Container sudah di-restart
- [ ] Lead memiliki email address yang valid
- [ ] Test kirim email ke diri sendiri dulu (opsional tapi disarankan)

---

## HASIL YANG DIHARAPKAN

Jika semua konfigurasi benar:

✅ Sender email: **ceklan62@gmail.com**
✅ Status: **Sent** atau **Open**
✅ Email diterima di inbox penerima
✅ Bisa reply balas ke ceklan62@gmail.com

---

## JIKA MASIH GAGAL

Jika setelah mengikuti semua langkah di atas masih gagal:

1. Cek log error di container
2. Verifikasi kembali App Password
3. Coba kirim ke email lain (bukan Gmail)
4. Hubungi provider hosting jika ada pembatasan SMTP
5. Cek apakah Google memblokir login (biasanya ada email notifikasi dari Google)

---

**Dibuat untuk**: Test dan verifikasi pengiriman email CRM
**Tanggal**: 2026-02-12
**File terkait**: 
- `crm/api/communication.py`
- `frontend/src/components/CommunicationArea.vue`
