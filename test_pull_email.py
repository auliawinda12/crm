import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Test the pull_incoming_emails function
    from crm.api.email import pull_incoming_emails
    pull_incoming_emails()
    print("Email pull completed!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    frappe.destroy()
