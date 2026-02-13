# -*- coding: utf-8 -*-
import frappe

frappe.init(site='crm.localhost')
frappe.connect()

try:
    frappe.db.commit()

    # Cari template email dan update
    email_templates = frappe.db.get_all('Email Template', fields=['name', 'response_html'])

    updated_count = 0
    for template in email_templates:
        html_content = template.get('response_html')

        if html_content and 'leave this conversation' in html_content.lower():
            html_content = html_content.replace('Leave this conversation to stop receiving emails of this type', '')
            html_content = html_content.replace('If you no longer wish to receive these emails, please leave this conversation.', '')
            html_content = html_content.replace('To stop receiving these emails, please leave this conversation.', '')
            html_content = html_content.replace('To unsubscribe, please leave this conversation.', '')

            # Jika setelah replace tidak ada teks lagi
            if not html_content.strip() or html_content == '<div>':
                html_content = ''

            template.response_html = html_content
            template.subject = template.get('subject').replace('Leave this conversation', '')
            template.save()
            frappe.db.commit()
            updated_count += 1
            print('Updated template: {}'.format(template.get('name')))

    print('Footer removed from {} email templates'.format(updated_count))

except Exception as e:
    print('Error: {}'.format(e))

finally:
    frappe.destroy()
