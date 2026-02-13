import frappe
from inspect import signature


def remove_email_footer(message):
	"""
	Remove 'Leave this conversation' footer from email message before sending.
	This footer is automatically added by Frappe but can be intrusive.
	"""
	if not message:
		return message

	footer_texts = [
		'Leave this conversation to stop receiving emails of this type',
		'If you no longer wish to receive these emails, please leave this conversation.',
		'To stop receiving these emails, please leave this conversation.',
		'To unsubscribe, please leave this conversation.',
	]

	# Remove footer variations
	for footer_text in footer_texts:
		message = message.replace(footer_text, '')
		# Also handle case variations
		message = message.replace(footer_text.lower(), '')
		message = message.replace(footer_text.upper(), '')

	return message.strip()


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

	# Remove "Leave this conversation" footer from message content
	if "message" in args and args["message"]:
		args["message"] = remove_email_footer(args["message"])

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

	# Remove footer from result communication content
	if result and isinstance(result, dict):
		# Clean message content
		if "message" in result and result["message"]:
			result["message"] = remove_email_footer(result["message"])
		# Clean subject if it contains footer text
		if "subject" in result and result["subject"]:
			result["subject"] = remove_email_footer(result["subject"])

		# FORCE update sender in the result communication document
		if default_email_account and default_email_account.get("email_id"):
			comm_name = result.get("name")
			if comm_name:
				frappe.db.set_value("Communication", comm_name, "sender", default_email_account["email_id"])
				# Also update content without footer
				if "message" in result:
					frappe.db.set_value("Communication", comm_name, "content", result["message"])
				frappe.db.commit()

	return result
