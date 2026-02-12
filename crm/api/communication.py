import frappe


@frappe.whitelist()
def make(args):
	"""
	Override communication email make function to use Default Outgoing Email Account as sender.
	This ensures emails are sent from the configured default outgoing email account
	instead of the logged-in user's email (e.g., Administrator).

	Args:
		args (dict): Communication arguments from frontend

	Returns:
		dict: Communication document data
	"""
	# Get default outgoing email account
	default_email_account = frappe.db.get_value(
		"Email Account", {"default_outgoing": 1, "enable_outgoing": 1}, ["email_id", "name"], as_dict=True
	)

	# If default outgoing email account exists, use it as sender
	if default_email_account and default_email_account.get("email_id"):
		args["sender"] = default_email_account["email_id"]
		# Set sender_full_name to None to let system use default
		args["sender_full_name"] = None
		# EXPLICITLY set sender again after any potential overrides
		args["_force_sender"] = default_email_account["email_id"]

	# Call the original make function from frappe
	from frappe.core.doctype.communication.email import make as original_make

	result = original_make(args)

	# FORCE update sender in the result communication document
	if default_email_account and default_email_account.get("email_id"):
		if result and isinstance(result, dict):
			comm_name = result.get("name")
			if comm_name:
				frappe.db.set_value("Communication", comm_name, "sender", default_email_account["email_id"])
				frappe.db.commit()

	return result
