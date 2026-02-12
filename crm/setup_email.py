import frappe


def setup_gmail_account():
	"""
	Setup Gmail Email Account for CRM.
	Run via: bench --site crm.localhost execute crm.setup_email.setup_gmail_account
	"""
	email_id = "ceklan62@gmail.com"
	app_password = "xwxl npnr urwu pazr"

	# Check if email account already exists
	existing = frappe.db.exists("Email Account", {"email_id": email_id})
	if existing:
		# Update existing email account
		doc = frappe.get_doc("Email Account", existing)
		doc.password = app_password
		doc.enable_outgoing = 1
		doc.default_outgoing = 1
		doc.enable_incoming = 1
		doc.default_incoming = 1
		doc.use_tls = 1
		doc.smtp_server = "smtp.gmail.com"
		doc.smtp_port = 587
		doc.email_server = "imap.gmail.com"
		doc.use_ssl = 1
		doc.use_imap = 1
		doc.save()
		print(f"Updated email account: {email_id}")
	else:
		# Remove default_outgoing flag from other accounts
		frappe.db.sql("UPDATE `tabEmail Account` SET default_outgoing = 0 WHERE default_outgoing = 1")
		frappe.db.sql("UPDATE `tabEmail Account` SET default_incoming = 0 WHERE default_incoming = 1")

		doc = frappe.get_doc({
			"doctype": "Email Account",
			"email_id": email_id,
			"email_account_name": "CRM Gmail",
			"service": "GMail",
			"password": app_password,
			"enable_outgoing": 1,
			"default_outgoing": 1,
			"enable_incoming": 1,
			"default_incoming": 1,
			"use_tls": 1,
			"smtp_server": "smtp.gmail.com",
			"smtp_port": 587,
			"email_server": "imap.gmail.com",
			"use_ssl": 1,
			"use_imap": 1,
			"email_sync_option": "ALL",
			"initial_sync_count": 100,
			"create_contact": 1,
			"track_email_status": 1,
			"always_use_account_email_id_as_sender": 1,
			"append_to": "CRM Lead",
		})
		doc.append("imap_folder", {"append_to": "CRM Lead", "folder_name": "INBOX"})
		doc.insert()
		print(f"Created email account: {email_id}")

	# Update Administrator user email
	admin_user = frappe.get_doc("User", "Administrator")
	if admin_user.email != email_id:
		# Update the email through direct SQL to avoid validation issues
		frappe.db.set_value("User", "Administrator", "email", email_id)
		print(f"Updated Administrator email to: {email_id}")

	# Disable mute_emails so emails are actually sent
	frappe.db.set_value("System Settings", "System Settings", "mute_emails", 0)
	print("Disabled mute_emails in System Settings")

	frappe.db.commit()
	print("\nEmail setup complete! Emails will now be sent from: " + email_id)
