import frappe

# Cek semua Email Account
all_accounts = frappe.db.get_all(
	"Email Account", fields=["name", "email_id", "default_outgoing", "enable_outgoing"], order_by="email_id"
)

print("=" * 70)
print("SETUP DEFAULT OUTGOING EMAIL ACCOUNT")
print("=" * 70)

print(f"\n[1] Mengecek semua Email Account yang ada...")
print(f"   Ditemukan {len(all_accounts)} Email Account:")

for acc in all_accounts:
	print(f"      - {acc.get('email_id')}")
	print(
		f"        Default Outgoing: {acc.get('default_outgoing')} | Enable Outgoing: {acc.get('enable_outgoing')}"
	)

# Cari ceklan62@gmail.com
print(f"\n[2] Mencari email account ceklan62@gmail.com...")
target_email = "ceklan62@gmail.com"
target_account = None

for acc in all_accounts:
	if acc.get("email_id") == target_email:
		target_account = acc
		break

if not target_account:
	print(f"   ❌ Email account {target_email} TIDAK DITEMUKAN!")
	print(f"   Silakan buat Email Account untuk {target_email} terlebih dahulu.")
else:
	print(f"   ✅ Ditemukan: {target_account.get('name')}")

	# Update ceklan62@gmail.com menjadi Default Outgoing
	print(f"\n[3] Mengatur {target_email} sebagai Default Outgoing...")

	frappe.db.set_value("Email Account", target_account.get("name"), "default_outgoing", 1)
	frappe.db.set_value("Email Account", target_account.get("name"), "enable_outgoing", 1)

	print(f"   ✅ Berhasil mengatur {target_email}:")
	print(f"      - Default Outgoing: 1 (Yes)")
	print(f"      - Enable Outgoing: 1 (Yes)")

	# Nonaktifkan Default Outgoing untuk email account lain
	print(f"\n[4] Menonaktifkan Default Outgoing untuk email account lain...")

	other_accounts = [acc for acc in all_accounts if acc.get("email_id") != target_email]
	updated_count = 0

	for acc in other_accounts:
		if acc.get("default_outgoing") == 1:
			frappe.db.set_value("Email Account", acc.get("name"), "default_outgoing", 0)
			print(f"   ✅ Nonaktifkan Default Outgoing untuk: {acc.get('email_id')}")
			updated_count += 1

	if updated_count == 0:
		print(f"   ℹ️  Tidak ada email account lain yang perlu dinonaktifkan")

	# Verifikasi
	print(f"\n[5] Verifikasi hasil perubahan...")
	frappe.db.commit()

	updated_accounts = frappe.db.get_all(
		"Email Account",
		fields=["name", "email_id", "default_outgoing", "enable_outgoing"],
		order_by="email_id",
	)

	default_outgoing_accounts = [acc for acc in updated_accounts if acc.get("default_outgoing") == 1]

	print(f"\n   Status Default Outgoing Email Account:")
	if len(default_outgoing_accounts) == 1 and default_outgoing_accounts[0].get("email_id") == target_email:
		print(f"   ✅ KONFIGURASI BENAR!")
		print(f"      Default Outgoing: {default_outgoing_accounts[0].get('email_id')}")
		print(f"      Enable Outgoing: {default_outgoing_accounts[0].get('enable_outgoing')}")
	elif len(default_outgoing_accounts) == 0:
		print(f"   ❌ TIDAK ADA Default Outgoing Email Account!")
	else:
		print(f"   ⚠️  PERINGATAN: Ada {len(default_outgoing_accounts)} Default Outgoing Email Account:")
		for acc in default_outgoing_accounts:
			print(f"      - {acc.get('email_id')}")

print("\n" + "=" * 70)
