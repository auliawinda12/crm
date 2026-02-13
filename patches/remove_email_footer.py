import frappe

def execute():
    """
    Patch to remove "Leave this conversation" footer from email templates
    """
    try:
        frappe.init(site='crm.localhost')
        frappe.connect()

        # Footer texts to remove
        footer_texts = [
            'Leave this conversation to stop receiving emails of this type',
            'If you no longer wish to receive these emails, please leave this conversation.',
            'To stop receiving these emails, please leave this conversation.',
            'To unsubscribe, please leave this conversation.'
        ]

        # Get all email templates
        templates = frappe.db.sql("SELECT name, response_html, subject FROM `tabEmail Template`", as_dict=True)

        updated_count = 0
        for template in templates:
            name = template.name
            html = template.response_html or ''
            subject = template.subject or ''

            modified = False

            # Remove footer from HTML
            for footer_text in footer_texts:
                if footer_text in html:
                    html = html.replace(footer_text, '')
                    modified = True

            # Remove footer from subject
            for footer_text in footer_texts:
                if footer_text in subject:
                    subject = subject.replace(footer_text, '')
                    modified = True

            # Clean up empty div tags
            if html.strip() == '<div>':
                html = ''

            # Update if modified
            if modified:
                frappe.db.sql(
                    "UPDATE `tabEmail Template` SET response_html = %s, subject = %s WHERE name = %s",
                    (html, subject, name)
                )
                updated_count += 1
                print(f'Updated template: {name}')

        frappe.db.commit()
        print(f'Successfully removed footer from {updated_count} email templates')

    except Exception as e:
        frappe.db.rollback()
        print(f'Error: {str(e)}')
        raise
    finally:
        frappe.destroy()

if __name__ == '__main__':
    execute()
