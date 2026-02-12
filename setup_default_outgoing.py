"""
Script untuk memverifikasi dan mengatur Default Outgoing Email Account.
Script ini akan:
1. Mengecek semua Email Account yang ada
2. Mengatur ceklan62@gmail.com sebagai Default Outgoing
3. Menonaktifkan Default Outgoing untuk email account lain
"""

import sys

import frappe


def setup_default_outgoing_email():
	"""Setup Default Outgoing Email Account"""

	print("=" * 70)
	print("SETUP DEFAULT OUTGOING EMAIL ACCOUNT")
	print("=" * 70)

	# 1. Cek semua Email Account
	print("\n[1] Mengecek semua Email Account yang ada...")
	all_accounts = frappe.db.get_all(
		"Email Account",
		fields=["name", "email_id", "default_outgoing", "enable_outgoing", "smtp_server"],
		order_by="email_id",
	)

	if not all_accounts:
		print("   ❌ TIDAK ADA Email Account yang ditemukan!")
		print("   Silakan buat Email Account terlebih dahulu.")
		return False

	print(f"   Ditemukan {len(all_accounts)} Email Account:")
	for acc in all_accounts:
		print(f"      - {acc.get('email_id')}")
		print(
			f"        Default Outgoing: {acc.get('default_outgoing')} | Enable Outgoing: {acc.get('enable_outgoing')}"
		)

	# 2. Cari ceklan62@gmail.com
	print("\n[2] Mencari email account ceklan62@gmail.com...")
	target_email = "ceklan62@gmail.com"
	target_account = None

	for acc in all_accounts:
		if acc.get("email_id") == target_email:
			target_account = acc
			break

	if not target_account:
		print(f"   ❌ Email account {target_email} TIDAK DITEMUKAN!")
		print(f"   Silakan buat Email Account untuk {target_email} terlebih dahulu.")
		return False

	print(f"   ✅ Ditemukan: {target_account.get('name')}")

	# 3. Update ceklan62@gmail8 menjadi Default Outgoing
	print(f"\n[3] Mengatur {target_email} sebagai Default Outgoing...")

	try:
		# Set default_outgoing = 1 untuk ceklan62@gmail.com
		frappe.db.set_value("Email Account", target_account.get("name"), "default_outgoing", 1)

		# Set enable_outgoing = 1 untuk ceklan62@gmail.com
		frappe.db.set_value("Email Account", target_account.get("name"), "enable_outgoing", 1)

		print(f"   ✅ Berhasil mengatur {target_email}:")
		print(f"      - Default Outgoing: 1 (Yes)")
		print(f"      - Enable Outgoing: 1 (Yes)")

	except Exception as e:
		print(f"   ❌ Gagal mengatur {target_email}: {str(e)}")
		return False

	# 4. Nonaktifkan Default Outgoing untuk email account lain
	print(f"\n[4] Menonaktifkan Default Outgoing untuk email account lain...")

	other_accounts = [acc for acc in all_accounts if acc.get("email_id") != target_email]
	updated_count = 0

	for acc in other_accounts:
		if acc.get("default_outgoing") == 1:
			try:
				frappe.db.set_value("Email Account", acc.get("name"), "default_outgoing", 0)
				print(f"   ✅ Nonaktifkan Default Outgoing untuk: {acc.get('email_id')}")
				updated_count += 1
			except Exception as e:
				print(f"   ❌ Gagal menonaktifkan {acc.get('email_id')}: {str(e)}")

	if updated_count == 0:
		print(f"   ℹ️  Tidak ada email account lain yang perlu dinonaktifkan")

	# 5. Verifikasi hasil
	print(f"\n[5] Verifikasi hasil perubahan...")

	frappe.db.commit()  # Commit semua perubahan

	# Refresh data
	updated_accounts = frappe.db.get_all(
		"Email Account",
		fields=["name", "email_id", "default_outgoing", "enable_outgoing", "smtp_server"],
		order_by="email_id",
	)

	default_outgoing_accounts = [acc for acc in updated_accounts if acc.get("default_outgoing") == 1]

	print(f"\n   Status Default Outging Email Account:")
	if len(default_outgoing_accounts) == 1 and default_outgoing_accounts[0].get("email_id") == target_email:
		print(f"   ✅ KONFIGURASI BENAR!")
		print(f"      Default Outgoing: {default_outgoing_accounts[0].get('email_id')}")
		print(f"      Enable Outgoing: {default_outgoing_accounts[0].get('enable_outgoing')}")
		return True
	elif len(default_outgoing_accounts) == 0:
		print(f"   ❌ TIDAK ADA Default Outgoing Email Account!")
		return False
	else:
		print(f"   ⚠️  PERINGATAN: Ada {len(default_outgoing_accounts)} Default Outging Email Account:")
		for acc in default_outgoing_accounts:
			print(f"      - {acc.get('email_id')}")
		print(f"   Seharusnya HANYA {target_email} yang menjadi Default Outgoing.")
		return False


if __name__ == "__main__":
	try:
		# Initialize frappe
		frappe.init(site="localhost")  # Sesuaikan dengan site name Anda
		frappe.connect()

		# Jalankan setup
		success = setup_default_outgoing_email()

		print("\n" + "=" * 70)
		if success:
			print("✅ SETUP BERHASIL!")
			print("\nKonfigurasi Email Account sudah benar:")
			print("  - Default Outgoing: ceklan62@gmail.com ✅")
			print("  - Enable Outgoing: Yes ✅")
			print("\nSekarang Anda bisa mengirim email dengan sender ceklan62@gmail.com")
		else:
			print("❌ SETUP GAGAL!")
			print("\nSilakan cek error di atas dan perbaiki konfigurasi.")
		print("=" * 70)

		sys.exit(0 if success else 1)

	except Exception as e:
		print(f"\n❌ FATAL ERROR: {str(e)}")
		import traceback

		traceback.print_exc()
		sys.exit(1)
	finally:
		frappe.destroy()
