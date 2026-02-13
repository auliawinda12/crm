#!/bin/bash
# Script to remove footer from email templates

cd //home/frappe/frappe-bench
bench --site crm.localhost execute "
import frappe
frappe.init(site='crm.localhost')
frappe.connect()

# Update template Indonesia
templates = frappe.db.sql(\"SELECT name, response_html FROM \\\`tabEmail Template\\` WHERE name = 'Email Template Indonesia' \\\"\")

for t in templates:
    name = t[0]
    html = t[1]

    # Remove footer texts
    if 'leave this conversation' in html.lower():
        html = html.replace(\"leave this conversation to stop receiving emails of this type\\\", \\\"\\\")
        html = html.replace(\"If you no longer wish to receive these emails, please leave this conversation.\\\", \\\"\\\")
        html = html.replace(\"To stop receiving these emails, please leave this conversation.\\\", \\\"\\\")
        html = html.replace(\"To unsubscribe, please leave this conversation.\\\", \\\"\\\")

    if not html.strip() or html == '<div>':
        html = \\\"\\\"

    # Update database
    frappe.db.sql(\"UPDATE \\\`tabEmail Template\\\` SET response_html = %s WHERE name = 'Email Template Indonesia' \\\\"\\\"\", (html,))
    frappe.db.sql(\"UPDATE \\\`tabEmail Template\\\` SET subject = \\\"\\\\\\\" WHERE name = 'Email Template Indonesia' \\\"\\\" \")
    frappe.db.commit()

    print('Footer removed from template Indonesia')
\"
