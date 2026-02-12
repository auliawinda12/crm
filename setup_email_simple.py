import frappe

# Setup ceklan62@gmail.com sebagai Default Outgoing
try:
	# Cari email account ceklan62@gmail.com
	email_account = frappe.db.get_value("Email Account", {"email_id": "ceklan62@gmail.com"}, "name")

	if email_account:
		# Set default_outgoing = 1
		frappe.db.set_value("Email Account", email_account, "default_outgoing", 1)
		frappe.db.set_value("Email Account", email_account, "enable_outgoing", 1)

		# Unset default_outgoing untuk email lain
		frappe.db.sql(
			"UPDATE `tabEmail Account` SET default_outgoing = 0 WHERE email_id != 'ceklan62@gmail.com'"
		)

		frappe.db.commit()

		print("SUCCESS: ceklan62@gmail8 telah diatur sebagai Default Outgoing Email Account")
		print("Default Outgoing: 1 (Checked)")
		print("Enable Outgoing: 1 (Checked)")
	else:
		print("ERROR: Email account ceklan62@gmail.com tidak ditemukan!")

except Exception as e:
	print(f"ERROR: {str(e)}")
