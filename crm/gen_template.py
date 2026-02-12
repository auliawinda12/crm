import frappe
import json

def test_import():
    """Test the Data Import with a sample CSV to understand how column mapping works."""
    
    # First, let's check what fields are available for import mapping
    from frappe.core.doctype.data_import.importer import ImportFile

    # Create a simple test CSV content
    csv_content = """ID,Salutation,First Name,Last Name,Company Name,Gender,Email Id,Is Primary (email),Phone,Is Primary Mobile No
,Mr,Test,User,PT Test Company,Male,test@test.com,1,+6280000000001,1"""

    # Create a Data Import document
    di = frappe.new_doc("Data Import")
    di.reference_doctype = "Contact"
    di.import_type = "Insert New Records"
    
    # Save the CSV as a file
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "test_import.csv",
        "content": csv_content,
        "is_private": 1,
    })
    file_doc.save(ignore_permissions=True)
    
    di.import_file = file_doc.file_url
    di.save(ignore_permissions=True)
    
    # Now check the template_options to see the column mapping
    print("=== Data Import Created ===")
    print(f"Name: {di.name}")
    print(f"Template Options: {di.template_options}")
    
    # Try to get preview
    di.get_preview_from_template(di.import_file)
    print(f"\nAfter preview:")
    print(f"Template Options: {di.template_options}")
    
    # Parse template_options
    if di.template_options:
        opts = json.loads(di.template_options)
        print(f"\nParsed Options:")
        print(json.dumps(opts, indent=2))
    
    # Clean up
    frappe.delete_doc("Data Import", di.name, force=True, ignore_permissions=True)
    frappe.delete_doc("File", file_doc.name, force=True, ignore_permissions=True)
    frappe.db.commit()
