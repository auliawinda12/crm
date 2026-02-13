import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Update email sync frequency to 60 seconds
    frappe.db.sql("""
        UPDATE `tabScheduled Job Type`
        SET frequency = '60'
        WHERE method = 'frappe.email.doctype.email_account.email_account.pull'
    """)
    frappe.db.commit()

    # Verify the update
    result = frappe.db.sql("""
        SELECT method, frequency
        FROM `tabScheduled Job Type`
        WHERE method LIKE '%email_account.pull%'
    """, as_dict=True)

    print("Email Sync Frequency Updated:")
    for row in result:
        print(f"- {row.get('method')}: {row.get('frequency')} seconds")

finally:
    frappe.destroy()
