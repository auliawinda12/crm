# -*- coding: utf-8 -*-
import frappe

# Connect to MariaDB using container credentials
conn = frappe.db.get_connection("mariadb")
cursor = conn.cursor()

try:
    # Commit any pending changes
    frappe.db.commit()

    # Cari template email dan update
    cursor.execute("SELECT name, response_html FROM `tabEmail Template`")
    templates = cursor.fetchall()

    updated_count = 0
    for template_name, html_content, subject in templates:
        html_content = html_content

        if "leave this conversation" in html_content.lower():
            html_content = html_content.replace("Leave this conversation to stop receiving emails of this type", "")
            html_content = html_content.replace("If you no longer wish to receive these emails, please leave this conversation.", "")
            html_content = html_content.replace("To stop receiving these emails, please leave this conversation.", "")
            html_content = html_content.replace("To unsubscribe, please leave this conversation.", "")

            # Jika setelah replace tidak ada teks lagi
            if not html_content.strip() or html_content == "<div>":
                html_content = ""

            # Update database - use backslash to escape strings
            cursor.execute("UPDATE `tabEmail Template` SET response_html = %s WHERE name = %s", (html_content,))
            cursor.execute("UPDATE `tabEmail Template` SET subject = %s WHERE name = %s", (subject.replace("Leave this conversation", ""),)
            frappe.db.commit()
            updated_count += 1
            print(f"Updated template: {template_name}")

    print(f"Footer removed from {updated_count} email templates")

except Exception as e:
    print(f"Error: {e}")
