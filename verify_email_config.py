import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Check email sync frequency
    result = frappe.db.sql("""
        SELECT method, frequency
        FROM `tabScheduled Job Type`
        WHERE method LIKE '%email_account.pull%'
    """, as_dict=True)

    print("=== EMAIL SYNC CONFIGURATION ===")
    for row in result:
        print(f"Method: {row.get('method')}")
        print(f"Frequency: {row.get('frequency')} seconds")
        print(f"\nEmails sync every {row.get('frequency')} seconds")
        print(f"Max wait time: ~{row.get('frequency')}-{int(row.get('frequency'))*2} seconds")

finally:
    frappe.destroy()
