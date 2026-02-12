"""
Simple script untuk mengubah email Administrator.
Jalankan dengan: docker exec crm-frappe-1 bash -c 'cd /home/frappe/frappe-bench/apps/crm && ./env/bin/python /tmp/change_admin_email.py'
"""

import sys
import os

# Add path
sys.path.insert(0, '/home/frappe/frappe-bench/apps/crm')

import frappe

frappe.init(site='crm.localhost', sites_path='sites')
frappe.connect()

new_email = sys.argv[1] if len(sys.argv) > 1 else input("Enter new email for Administrator: ")

print(f"Updating Administrator email to: {new_email}")

frappe.db.set_value('User', 'Administrator', {
    'email': new_email,
    'username': new_email
})
frappe.db.commit()

print("Success! Administrator email updated.")
print(f"New email: {new_email}")

frappe.destroy()
