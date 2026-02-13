import frappe


@frappe.whitelist()
def get_admin_email():
	"""
	Get the current email address for Administrator user.

	Returns:
		dict: Dictionary containing the Administrator's email
	"""
	admin_email = frappe.db.get_value("User", "Administrator", "email")
	return {"email": admin_email}


@frappe.whitelist()
def update_admin_email(new_email):
	"""
	Update the email address for the Administrator user.

	Args:
		new_email (str): The new email address for Administrator

	Returns:
		dict: Success message
	"""
	# Validate email format
	if not new_email or "@" not in new_email:
		frappe.throw("Invalid email address")

	# Check if email already exists for another user
	existing_user = frappe.db.get_value("User", {"email": new_email, "name": ["!=", "Administrator"]}, "name")
	if existing_user:
		frappe.throw("This email is already in use by another user")

	# Update Administrator email
	try:
		frappe.db.set_value("User", "Administrator", {
			"email": new_email,
			"username": new_email
		})
		frappe.db.commit()

		return {
			"success": True,
			"message": f"Administrator email updated to {new_email}"
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.throw(f"Failed to update email: {str(e)}")


@frappe.whitelist()
def create_email_account(data):
	service = data.get("service")
	service_config = email_service_config.get(service)
	if not service_config:
		return "Service not supported"

	try:
		email_doc = frappe.get_doc(
			{
				"doctype": "Email Account",
				"email_id": data.get("email_id"),
				"email_account_name": data.get("email_account_name"),
				"service": service,
				"enable_incoming": data.get("enable_incoming"),
				"enable_outgoing": data.get("enable_outgoing"),
				"default_incoming": data.get("default_incoming"),
				"default_outgoing": data.get("default_outgoing"),
				"email_sync_option": "ALL",
				"initial_sync_count": 100,
				"create_contact": 1,
				"track_email_status": 1,
				"use_tls": 1,
				"use_imap": 1,
				"smtp_port": 587,
				**service_config,
			}
		)
		if service == "Frappe Mail":
			email_doc.api_key = data.get("api_key")
			email_doc.api_secret = data.get("api_secret")
			email_doc.frappe_mail_site = data.get("frappe_mail_site")
			email_doc.append_to = "Communication"
		else:
			email_doc.append("imap_folder", {"append_to": "Communication", "folder_name": "INBOX"})
			email_doc.password = data.get("password")
			# validate whether the credentials are correct
			email_doc.get_incoming_server()

		# if correct credentials, save the email account
		email_doc.save()
	except Exception as e:
		frappe.throw(str(e))


email_service_config = {
	"Frappe Mail": {
		"domain": None,
		"password": None,
		"awaiting_password": 0,
		"ascii_encode_password": 0,
		"login_id_is_different": 0,
		"login_id": None,
		"use_imap": 0,
		"use_ssl": 0,
		"validate_ssl_certificate": 0,
		"use_starttls": 0,
		"email_server": None,
		"incoming_port": 0,
		"always_use_account_email_id_as_sender": 1,
		"use_tls": 0,
		"use_ssl_for_outgoing": 0,
		"smtp_server": None,
		"smtp_port": None,
		"no_smtp_authentication": 0,
	},
	"GMail": {
		"email_server": "imap.gmail.com",
		"use_ssl": 1,
		"smtp_server": "smtp.gmail.com",
	},
	"Outlook": {
		"email_server": "imap-mail.outlook.com",
		"use_ssl": 1,
		"smtp_server": "smtp-mail.outlook.com",
	},
	"Sendgrid": {
		"smtp_server": "smtp.sendgrid.net",
		"smtp_port": 587,
	},
	"SparkPost": {
		"smtp_server": "smtp.sparkpostmail.com",
	},
	"Yahoo": {
		"email_server": "imap.mail.yahoo.com",
		"use_ssl": 1,
		"smtp_server": "smtp.mail.yahoo.com",
		"smtp_port": 587,
	},
	"Yandex": {
		"email_server": "imap.yandex.com",
		"use_ssl": 1,
		"smtp_server": "smtp.yandex.com",
		"smtp_port": 587,
	},
}
