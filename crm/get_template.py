import frappe
import json

def get_import_template():
    """Check the correct Data Import template headers for Contact doctype."""
    # Check Frappe version data import
    from frappe.core.doctype.data_import.importer import Importer

    # Get the template columns
    doctype = "Contact"
    meta = frappe.get_meta(doctype)

    print("=== CONTACT PARENT FIELDS ===")
    for f in meta.fields:
        if f.fieldtype not in ("Section Break", "Column Break", "Tab Break", "Table"):
            print(f"  {f.fieldname} ({f.fieldtype}) - label: {f.label}")

    print("\n=== CHILD TABLES ===")
    for f in meta.fields:
        if f.fieldtype == "Table":
            print(f"\nChild Table: {f.fieldname} -> {f.options}")
            child_meta = frappe.get_meta(f.options)
            for cf in child_meta.fields:
                if cf.fieldtype not in ("Section Break", "Column Break"):
                    print(f"  - {cf.fieldname} ({cf.fieldtype}) - label: {cf.label}")

    # Try to generate template
    print("\n=== DATA IMPORT TEMPLATE HEADERS ===")
    try:
        di = frappe.new_doc("Data Import")
        di.reference_doctype = "Contact"
        di.import_type = "Insert New Records"

        header_row = ["ID"]
        header_row.append("first_name")
        header_row.append("last_name")
        header_row.append("salutation")
        header_row.append("company_name")
        header_row.append("gender")
        header_row.append("address")
        header_row.append("ID (Contact Email)")
        header_row.append("email_id (Contact Email)")
        header_row.append("is_primary (Contact Email)")
        header_row.append("ID (Contact Phone)")
        header_row.append("phone (Contact Phone)")
        header_row.append("is_primary_mobile_no (Contact Phone)")

        print("Suggested headers:")
        print(",".join(header_row))
    except Exception as e:
        print(f"Error: {e}")

    # Also check existing contacts to see what their data looks like
    print("\n=== SAMPLE EXISTING CONTACT ===")
    contacts = frappe.get_all("Contact", limit=1)
    if contacts:
        doc = frappe.get_doc("Contact", contacts[0].name)
        print(f"Name: {doc.name}")
        print(f"email_id: {doc.email_id}")
        print(f"mobile_no: {doc.mobile_no}")
        print(f"email_ids: {json.dumps([{'email_id': e.email_id, 'is_primary': e.is_primary} for e in doc.email_ids], indent=2)}")
        print(f"phone_nos: {json.dumps([{'phone': p.phone, 'is_primary_mobile_no': p.is_primary_mobile_no} for p in doc.phone_nos], indent=2)}")
