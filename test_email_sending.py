"""
Test script untuk menguji pengiriman email melalui CRM.
Script ini akan mengirim test email dan menampilkan hasilnya.
"""

import frappe


def test_email_sending():
	"""Test pengiriman email dengan Default Outgoing Email Account"""

	print("=" * 60)
	print("TEST PENGIRIMAN EMAIL CRM")
	print("=" * 60)

	# 1. Cek Default Outgoing Email Account
	print("\n[1] Mengecek Default Outgoing Email Account...")
	default_email = frappe.db.get_value(
		"Email Account",
		{"default_outgoing": 1, "enable_outgoing": 1},
		["name", "email_id", "smtp_server", "smtp_port", "enable_outgoing"],
		as_dict=True,
	)

	if not default_email:
		print("   ❌ TIDAK ADA Default Outgoing Email Account!")
		print("   Silakan set Default Outgoing di Email Account terlebih dahulu.")
		return False
	else:
		print("   ✅ Default Outgoing Email Account ditemukan:")
		print(f"      - Name: {default_email.get('name')}")
		print(f"      - Email ID: {default_email.get('email_id')}")
		print(f"      - SMTP Server: {default_email.get('smtp_server')}")
		print(f"      - SMTP Port: {default_email.get('smtp_port')}")
		print(f"      - Enable Outgoing: {default_email.get('enable_outgoing')}")

	# 2. Cek user Administrator
	print("\n[2] Mengecek User Administrator...")
	admin_email = frappe.db.get_value("User", "Administrator", "email")
	print(f"   Administrator Email: {admin_email}")

	# 3. Test panggil API CRM
	print("\n[3] Test panggil API crm.api.communication.make...")
	try:
		from crm.api.communication import make

		# Siapkan test data
		test_args = {
			"recipients": admin_email,  # Kirim ke admin sendiri untuk test
			"subject": "CRM Email Test - Email dari Default Outgoing",
			"content": """
            <div style="font-family: Arial, sans-serif; max-width: 600px;">
                <h2 style="color: #007bff;">Test Email CRM</h2>
                <p>Ini adalah email test untuk memverifikasi pengiriman email.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>From:</strong> Default Outgoing Email Account</p>
                    <p style="margin: 5px 0;"><strong>To:</strong> Administrator</p>
                    <p style="margin: 5px 0;"><strong>Purpose:</strong> Test pengiriman email</p>
                </div>
                <p style="color: #666; font-size: 12px;">Jika Anda menerima email ini, berarti konfigurasi email sudah benar.</p>
            </div>
            """,
			"doctype": "User",
			"name": "Administrator",
			"send_email": 1,
		}

		print("   Mengirim email test...")
		result = make(test_args)

		if result:
			print("   ✅ Email berhasil dikirim!")
			print(f"      Communication Name: {result.get('name')}")
			print(f"      Status: {result.get('status')}")
			print(f"      Sender: {result.get('sender')}")
			return True
		else:
			print("   ❌ Gagal mengirim email - tidak ada response")
			return False

	except Exception as e:
		print(f"   ❌ Error saat mengirim email: {str(e)}")
		import traceback

		print("\n   Traceback:")
		traceback.print_exc()
		return False

	# 4. Cek Email Queue
	print("\n[4] Mengecek Email Queue...")
	email_queue = frappe.db.get_all(
		"Email Queue", fields=["name", "status", "creation"], order_by="creation desc", limit=5
	)

	if email_queue:
		print(f"   Ditemukan {len(email_queue)} email terbaru di queue:")
		for queue in email_queue:
			print(
				f"      - {queue.get('name')} | Status: {queue.get('status')} | Created: {queue.get('creation')}"
			)
	else:
		print("   Tidak ada email di queue")

	# 5. Cek Email Log
	print("\n[5] Mengecek Email Log...")
	email_log = frappe.db.get_all(
		"Email Log",
		fields=["name", "status", "sender", "recipient", "creation"],
		order_by="creation desc",
		limit=5,
	)

	if email_log:
		print(f"   Ditemukan {len(email_log)} log email terbaru:")
		for log in email_log:
			print(
				f"      - From: {log.get('sender')} | To: {log.get('recipient')} | Status: {log.get('status')}"
			)
	else:
		print("   Tidak ada log email")

	print("\n" + "=" * 60)
	print("TEST SELESAI")
	print("=" * 60)


if __name__ == "__main__":
	try:
		# Initialize frappe
		frappe.init(site="localhost")  # Sesuaikan dengan site name Anda
		frappe.connect()

		# Jalankan test
		success = test_email_sending()

		if success:
			print("\n✅ TEST BERHASIL - Email dapat dikirim dari Default Outgoing Account!")
			print("\nSekarang Anda bisa mencoba mengirim email ke lead Mr Teuku Audi.")
		else:
			print("\n❌ TEST GAGAL - Silakan cek error di atas dan perbaiki konfigurasi.")

	except Exception as e:
		print(f"\n❌ FATAL ERROR: {str(e)}")
		import traceback

		traceback.print_exc()
	finally:
		frappe.destroy()
