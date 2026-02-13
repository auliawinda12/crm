import frappe
from inspect import signature


@frappe.whitelist()
def make(args=None, **kwargs):
	"""
	Override communication email make function to use Default Outgoing Email Account as sender.
	This ensures emails are sent from the configured default outgoing email account
	instead of the logged-in user's email (e.g., Administrator).

	Args:
		args (dict): Communication arguments from frontend

	Returns:
		dict: Communication document data
	"""
	# Support both payload styles:
	# 1) {"args": {...}} and 2) direct kwargs from frontend call(...)
	if args is None:
		args = kwargs
	elif isinstance(args, str):
		args = frappe.parse_json(args)

	if not isinstance(args, dict):
		frappe.throw("Invalid arguments for communication.make")

	args = dict(args)
	# Internal frappe RPC metadata; must not be forwarded to email.make
	args.pop("cmd", None)

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

	# Frappe versions differ:
	# - older: make(args)
	# - newer: make(**kwargs)
	params = signature(original_make).parameters
	if "args" in params and len(params) == 1:
		result = original_make(args)
	else:
		result = original_make(**args)

	# FORCE update sender in the result communication document
	if default_email_account and default_email_account.get("email_id"):
		if result and isinstance(result, dict):
			comm_name = result.get("name")
			if comm_name:
				frappe.db.set_value("Communication", comm_name, "sender", default_email_account["email_id"])
				frappe.db.commit()

	return result
