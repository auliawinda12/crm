import frappe

# Setup ceklan62@gmail.com sebagai Default Outgoing
acc = frappe.db.get_value(
	"Email Account",
	{"email_id": "ceklan62@gmail.com"},
	["name", "default_outgoing", "enable_outgoing"],
	as_dict=True,
)
print(f"Email Account sebelum update: {acc}")

if acc:
	# Set default_outgoing dan enable_outgoing ke 1
	frappe.db.set_value("Email Account", acc.get("name"), "default_outgoing", 1)
	frappe.db.set_value("Email Account", acc.get("name"), "enable_outgoing", 1)

	# Unset default_outgoing untuk email lain
	frappe.db.sql(
		"UPDATE `tabEmail Account` SET default_outgoing = 0 WHERE email_id != %s", "ceklan62@gmail.com"
	)

	frappe.db.commit()
	print("SUCCESS: ceklan62@gmail.com telah diatur sebagai Default Outgoing Email Account")
	print("Default Outgoing: 1 (Checked)")
	print("Enable Outgoing: 1 (Checked)")
else:
	print("ERROR: Email account ceklan62@gmail.com tidak ditemukan!")
