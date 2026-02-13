#!/usr/bin/env python3
"""
Standalone script to remove "Leave this conversation" footer from email templates.
Run this directly with: python run_footer_removal.py
"""

def remove_footer_from_templates():
	"""Connect to Frappe and remove footer from all email templates."""
	try:
		import frappe

		frappe.init(site='crm.localhost')
		frappe.connect()

		# Footer texts to remove
		footer_texts = [
			'Leave this conversation to stop receiving emails of this type',
			'If you no longer wish to receive these emails, please leave this conversation.',
			'To stop receiving these emails, please leave this conversation.',
			'To unsubscribe, please leave this conversation.',
		]

		print("Removing footer from Email Templates...")
		print("-" * 50)

		# Get all email templates
		templates = frappe.db.get_all("Email Template", fields=["name", "response_html", "subject", "html"])

		updated_count = 0
		for template in templates:
			modified = False
			html = template.get("response_html") or ""
			subject = template.get("subject") or ""
			template_html = template.get("html") or ""

			# Remove footer from response_html
			for footer_text in footer_texts:
				if footer_text in html:
					html = html.replace(footer_text, "")
					modified = True
				if footer_text.lower() in html.lower():
					html = html.replace(footer_text.lower(), "")
					modified = True

			# Remove footer from subject
			for footer_text in footer_texts:
				if footer_text in subject:
					subject = subject.replace(footer_text, "")
					modified = True
				if footer_text.lower() in subject.lower():
					subject = subject.replace(footer_text.lower(), "")
					modified = True

			# Remove footer from html
			for footer_text in footer_texts:
				if footer_text in template_html:
					template_html = template_html.replace(footer_text, "")
					modified = True
				if footer_text.lower() in template_html.lower():
					template_html = template_html.replace(footer_text.lower(), "")
					modified = True

			# Clean up empty div tags
			if html.strip() in ("<div>", "<div></div>", ""):
				html = ""

			# Update if modified
			if modified:
				frappe.db.set_value("Email Template", template.name, {
					"response_html": html,
					"subject": subject,
					"html": template_html
				})
				updated_count += 1
				print(f"  ✓ Updated: {template.name}")

		frappe.db.commit()
		print("-" * 50)
		print(f"✓ Footer removed from {updated_count} email templates")
		print()

		# Also update Communication records
		print("Removing footer from Communication records...")
		print("-" * 50)

		communications = frappe.db.get_all("Communication", {
			"communication_medium": "Email",
			"sent_or_received": "Sent"
		}, fields=["name", "content", "subject"])

		comm_updated = 0
		for comm in communications:
			modified = False
			content = comm.get("content") or ""
			subject = comm.get("subject") or ""

			for footer_text in footer_texts:
				if footer_text in content:
					content = content.replace(footer_text, "")
					modified = True
				if footer_text in subject:
					subject = subject.replace(footer_text, "")
					modified = True

			if modified:
				frappe.db.set_value("Communication", comm.name, {
					"content": content,
					"subject": subject
				})
				comm_updated += 1
				print(f"  ✓ Updated: {comm.name}")

		frappe.db.commit()
		print("-" * 50)
		print(f"✓ Footer removed from {comm_updated} communication records")
		print()

		frappe.destroy()

		print("=" * 50)
		print("SUCCESS: Footer removal completed!")
		print("=" * 50)
		print()
		print("Note: New emails will also have footer removed via:")
		print("  - crm/api/communication.py override")
		print("  - hooks.py before_send event")
		print()

	except ImportError:
		print("ERROR: Frappe module not found.")
		print("Please run this script inside the Frappe container or bench environment.")
		print()
		print("To run via Docker:")
		print("  docker compose exec frappe python /path/to/run_footer_removal.py")
		print()
	except Exception as e:
		print(f"ERROR: {str(e)}")
		raise


if __name__ == "__main__":
	remove_footer_from_templates()
