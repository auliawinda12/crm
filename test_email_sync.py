import frappe

# Initialize frappe
frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Pull emails from the email account
    email_account = frappe.get_doc("Email Account", "ceklan62@gmail.com")
    print("Pulling emails from Gmail...")

    email_account.pull(wait=True)
    print("Email sync completed successfully!")
except Exception as e:
    print(f"Error during sync: {e}")
    import traceback
    traceback.print_exc()
finally:
    frappe.destroy()
