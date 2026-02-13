import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Get all scheduled jobs related to email
    jobs = frappe.db.sql("""
        SELECT name, method, frequency
        FROM `tabScheduled Job Type`
        WHERE method LIKE '%email%' OR method LIKE '%pull%'
    """, as_dict=True)

    print("Current Email Sync Jobs:")
    for job in jobs:
        print(f"- {job.get('method')}: {job.get('frequency')}")

    # Update email sync frequency to 1 minute (60 seconds)
    frappe.db.sql("""
        UPDATE `tabScheduled Job Type`
        SET frequency = '60'
        WHERE method = 'email_account.pull_email_account'
    """)

    print("\nUpdated email sync frequency to 60 seconds")

    # Verify the update
    updated = frappe.db.sql("""
        SELECT name, method, frequency
        FROM `tabScheduled Job Type`
        WHERE method = 'email_account.pull_email_account'
    """, as_dict=True)

    print("\nNew Email Sync Settings:")
    for job in updated:
        print(f"- {job.get('method')}: {job.get('frequency')} seconds")

finally:
    frappe.destroy()
