import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Check if cron job already exists
    exists = frappe.db.exists("Scheduled Job Type", {"method": "crm.api.email.pull_incoming_emails"})

    if not exists:
        # Get the next idx
        max_idx = frappe.db.sql("SELECT MAX(idx) as max_idx FROM `tabScheduled Job Type`", as_dict=True)[0].get('max_idx') or 0

        # Insert the cron job for email sync every minute
        frappe.db.sql("""
            INSERT INTO `tabScheduled Job Type`
            (name, method, cron_format, paused, creation, modified, modified_by, owner, docstatus, idx, doctype)
            VALUES (%s, %s, %s, 0, NOW(), NOW(), 'Administrator', 'Administrator', 0, %s, 'Scheduled Job Type')
        """, ("crm.api.email.pull_incoming_emails", "crm.api.email.pull_incoming_emails", "* * * * *", max_idx + 1))

        frappe.db.commit()
        print("Created cron job: crm.api.email.pull_incoming_emails (runs every minute)")
    else:
        print("Cron job already exists")

    # List all CRM scheduled jobs
    jobs = frappe.db.sql("""
        SELECT method, cron_format
        FROM `tabScheduled Job Type`
        WHERE method LIKE 'crm.api.email%' OR method LIKE 'crm.lead_syncing%'
        ORDER BY idx
    """, as_dict=True)

    print("\nCurrent CRM Scheduled Jobs:")
    for job in jobs:
        print(f"- {job.get('method')}: {job.get('cron_format') or 'default frequency'}")

finally:
    frappe.destroy()
