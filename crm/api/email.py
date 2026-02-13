import frappe


def pull_incoming_emails():
	"""
	Pull incoming emails from all email accounts with enabled incoming.
	This runs every minute via cron job to ensure near real-time email sync.
	"""
	try:
		# Get all email accounts with incoming enabled
		email_accounts = frappe.get_all(
			"Email Account",
			filters={"enable_incoming": 1},
			fields=["name", "email_id"]
		)

		for account in email_accounts:
			try:
				email_account = frappe.get_doc("Email Account", account.get("name"))
				email_account.pull()
				frappe.logger().info(f"Pulled emails for {account.get('email_id')}")
			except Exception as e:
				frappe.logger().error(f"Error pulling emails for {account.get('email_id')}: {str(e)}")

	except Exception as e:
		frappe.logger().error(f"Error in pull_incoming_emails: {str(e)}")
