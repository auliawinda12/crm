import frappe

# Update IMAP folder append_to setting
doc = frappe.get_doc("Email Account", "ceklan62@gmail.com")
print(f"Current append_to: {doc.imap_folder[0].append_to}")

# Update to CRM Lead
doc.imap_folder[0].append_to = "CRM Lead"
doc.save()

print("Updated append_to to CRM Lead")
print("Incoming emails will now be linked to CRM Leads")
