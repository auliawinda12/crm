"""
Delete all existing dummy contacts.
Run via: bench --site crm.localhost execute crm.delete_contacts.delete_all_contacts
"""

import frappe


def delete_all_contacts():
    contacts = frappe.get_all("Contact", fields=["name", "first_name", "last_name"])
    count = 0
    for c in contacts:
        if c.name == "Administrator":
            continue
        frappe.delete_doc("Contact", c.name, force=True, ignore_permissions=True)
        print(f"Deleted: {c.first_name} {c.last_name}")
        count += 1
    frappe.db.commit()
    print(f"\nDeleted {count} contacts.")
