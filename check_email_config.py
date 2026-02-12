import frappe

# Cek semua Email Account
print("\n=== SEMUA EMAIL ACCOUNT ===")
all_accounts = frappe.db.get_all(
	"Email Account", fields=["name", "email_id", "default_outgoing", "enable_outgoing"]
)
for acc in all_accounts:
	print(f"Email: {acc.get('email_id')}")
	print(f"  Default Outgoing: {acc.get('default_outgoing')}")
	print(f"  Enable Outgoing: {acc.get('enable_outgoing')}")

# Cek Default Outgoing
print("\n=== DEFAULT OUTGOING EMAIL ACCOUNT ===")
default_acc = frappe.db.get_value(
	"Email Account", {"default_outgoing": 1}, ["email_id", "enable_outgoing"], as_dict=True
)
if default_acc:
	print(f"Default Outgoing Email: {default_acc.get('email_id')}")
	print(f"Enable Outgoing: {default_acc.get('enable_outgoing')}")
else:
	print("TIDAK ADA Default Outgoing Email Account!")

# User Administrator
print("\n=== ADMINISTRATOR USER ===")
admin_email = frappe.db.get_value("User", "Administrator", "email")
print(f"Administrator Email: {admin_email}")
