"""
Script to fix imported contacts that are missing email, phone, and address data.
Run via: bench --site <site_name> execute crm.fix_contacts.fix_imported_contacts
"""

import frappe


def fix_imported_contacts():
	"""Fix contacts imported from CSV that have missing email_id and mobile_no."""

	# Data from the CSV import
	contacts_data = [
		{"first_name": "Budi", "last_name": "Santoso", "email": "budi.santoso@email.com", "phone": "+6281234567890", "company": "PT Maju Jaya"},
		{"first_name": "Siti", "last_name": "Rahayu", "email": "siti.rahayu@email.com", "phone": "+6281234567891", "company": "CV Sejahtera"},
		{"first_name": "Andi", "last_name": "Wijaya", "email": "andi.wijaya@email.com", "phone": "+6281234567892", "company": "PT Teknologi Nusantara"},
		{"first_name": "Dewi", "last_name": "Lestari", "email": "dewi.lestari@email.com", "phone": "+6281234567893", "company": "Toko Sukses Makmur"},
		{"first_name": "Agus", "last_name": "Pratama", "email": "agus.pratama@email.com", "phone": "+6281234567894", "company": "PT Global Trade"},
		{"first_name": "Rina", "last_name": "Mulyani", "email": "rina.mulyani@email.com", "phone": "+6281234567895", "company": "PT Digital Indonesia"},
		{"first_name": "Eko", "last_name": "Saputra", "email": "eko.saputra@email.com", "phone": "+6281234567896", "company": "CV Berkah Abadi"},
		{"first_name": "Fitriani", "last_name": "Sari", "email": "fitriani.sari@email.com", "phone": "+6281234567897", "company": "PT Mandiri Sejahtera"},
		{"first_name": "Hendra", "last_name": "Setiawan", "email": "hendra.setiawan@email.com", "phone": "+6281234567898", "company": "PT Inovasi Teknologi"},
		{"first_name": "Indah", "last_name": "Pertiwi", "email": "indah.pertiwi@email.com", "phone": "+6281234567899", "company": "PT Sumber Rejeki"},
		{"first_name": "Joko", "last_name": "Susilo", "email": "joko.susilo@email.com", "phone": "+6281234567900", "company": "CV Unggul Jaya"},
		{"first_name": "Kartika", "last_name": "Sari", "email": "kartika.sari@email.com", "phone": "+6281234567901", "company": "PT Bangun Karya"},
		{"first_name": "Lukman", "last_name": "Hakim", "email": "lukman.hakim@email.com", "phone": "+6281234567902", "company": "PT Sejahtera Bersama"},
		{"first_name": "Maya", "last_name": "Sari", "email": "maya.sari@email.com", "phone": "+6281234567903", "company": "Toko Berkah Selalu"},
		{"first_name": "Nurul", "last_name": "Hidayat", "email": "nurul.hidayat@email.com", "phone": "+6281234567904", "company": "PT Kreatif Solusi"},
	]

	fixed = 0
	skipped = 0

	for data in contacts_data:
		# Find the contact by first_name and last_name
		contacts = frappe.get_all(
			"Contact",
			filters={"first_name": data["first_name"], "last_name": data["last_name"]},
			fields=["name"],
		)

		if not contacts:
			print(f"Contact not found: {data['first_name']} {data['last_name']}")
			skipped += 1
			continue

		contact = frappe.get_doc("Contact", contacts[0].name)

		# Check if email_ids child table is empty
		if not contact.email_ids:
			contact.append("email_ids", {
				"email_id": data["email"],
				"is_primary": 1,
			})

		# Check if phone_nos child table is empty
		if not contact.phone_nos:
			contact.append("phone_nos", {
				"phone": data["phone"],
				"is_primary_mobile_no": 1,
			})

		# Save the contact — this triggers before_save which computes email_id & mobile_no
		contact.save(ignore_permissions=True)
		print(f"Fixed: {data['first_name']} {data['last_name']} -> email: {contact.email_id}, mobile: {contact.mobile_no}")
		fixed += 1

	frappe.db.commit()
	print(f"\nDone! Fixed: {fixed}, Skipped: {skipped}")
