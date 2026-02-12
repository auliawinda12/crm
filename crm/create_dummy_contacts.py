"""
Script to create dummy contacts with all fields properly populated.
Run via: bench --site crm.localhost execute crm.create_dummy_contacts.create_contacts
"""

import frappe


def create_contacts():
	"""Create dummy contacts with email, phone, and address properly set."""

	contacts_data = [
		{
			"salutation": "Mr",
			"first_name": "Budi",
			"last_name": "Santoso",
			"email": "budi.santoso@email.com",
			"phone": "+6281234567890",
			"company_name": "PT Maju Jaya",
			"gender": "Male",
			"address_line1": "Jl. Sudirman No. 10",
			"city": "Jakarta Pusat",
		},
		{
			"salutation": "Ms",
			"first_name": "Siti",
			"last_name": "Rahayu",
			"email": "siti.rahayu@email.com",
			"phone": "+6281234567891",
			"company_name": "CV Sejahtera",
			"gender": "Female",
			"address_line1": "Jl. Gatot Subroto No. 25",
			"city": "Jakarta Selatan",
		},
		{
			"salutation": "Mr",
			"first_name": "Andi",
			"last_name": "Wijaya",
			"email": "andi.wijaya@email.com",
			"phone": "+6281234567892",
			"company_name": "PT Teknologi Nusantara",
			"gender": "Male",
			"address_line1": "Jl. Thamrin No. 5",
			"city": "Jakarta Pusat",
		},
		{
			"salutation": "Ms",
			"first_name": "Dewi",
			"last_name": "Lestari",
			"email": "dewi.lestari@email.com",
			"phone": "+6281234567893",
			"company_name": "Toko Sukses Makmur",
			"gender": "Female",
			"address_line1": "Jl. Diponegoro No. 15",
			"city": "Bandung",
		},
		{
			"salutation": "Mr",
			"first_name": "Agus",
			"last_name": "Pratama",
			"email": "agus.pratama@email.com",
			"phone": "+6281234567894",
			"company_name": "PT Global Trade",
			"gender": "Male",
			"address_line1": "Jl. Ahmad Yani No. 8",
			"city": "Surabaya",
		},
		{
			"salutation": "Ms",
			"first_name": "Rina",
			"last_name": "Mulyani",
			"email": "rina.mulyani@email.com",
			"phone": "+6281234567895",
			"company_name": "PT Digital Indonesia",
			"gender": "Female",
			"address_line1": "Jl. Malioboro No. 30",
			"city": "Yogyakarta",
		},
		{
			"salutation": "Mr",
			"first_name": "Eko",
			"last_name": "Saputra",
			"email": "eko.saputra@email.com",
			"phone": "+6281234567896",
			"company_name": "CV Berkah Abadi",
			"gender": "Male",
			"address_line1": "Jl. Pemuda No. 12",
			"city": "Semarang",
		},
		{
			"salutation": "Ms",
			"first_name": "Fitriani",
			"last_name": "Sari",
			"email": "fitriani.sari@email.com",
			"phone": "+6281234567897",
			"company_name": "PT Mandiri Sejahtera",
			"gender": "Female",
			"address_line1": "Jl. Imam Bonjol No. 22",
			"city": "Medan",
		},
		{
			"salutation": "Mr",
			"first_name": "Hendra",
			"last_name": "Setiawan",
			"email": "hendra.setiawan@email.com",
			"phone": "+6281234567898",
			"company_name": "PT Inovasi Teknologi",
			"gender": "Male",
			"address_line1": "Jl. Pahlawan No. 7",
			"city": "Denpasar",
		},
		{
			"salutation": "Ms",
			"first_name": "Indah",
			"last_name": "Pertiwi",
			"email": "indah.pertiwi@email.com",
			"phone": "+6281234567899",
			"company_name": "PT Sumber Rejeki",
			"gender": "Female",
			"address_line1": "Jl. Veteran No. 18",
			"city": "Makassar",
		},
		{
			"salutation": "Mr",
			"first_name": "Joko",
			"last_name": "Susilo",
			"email": "joko.susilo@email.com",
			"phone": "+6281234567900",
			"company_name": "CV Unggul Jaya",
			"gender": "Male",
			"address_line1": "Jl. Kartini No. 9",
			"city": "Malang",
		},
		{
			"salutation": "Ms",
			"first_name": "Kartika",
			"last_name": "Dewi",
			"email": "kartika.dewi@email.com",
			"phone": "+6281234567901",
			"company_name": "PT Bangun Karya",
			"gender": "Female",
			"address_line1": "Jl. Merdeka No. 33",
			"city": "Palembang",
		},
		{
			"salutation": "Mr",
			"first_name": "Lukman",
			"last_name": "Hakim",
			"email": "lukman.hakim@email.com",
			"phone": "+6281234567902",
			"company_name": "PT Sejahtera Bersama",
			"gender": "Male",
			"address_line1": "Jl. Hayam Wuruk No. 14",
			"city": "Surakarta",
		},
		{
			"salutation": "Ms",
			"first_name": "Maya",
			"last_name": "Anggraini",
			"email": "maya.anggraini@email.com",
			"phone": "+6281234567903",
			"company_name": "Toko Berkah Selalu",
			"gender": "Female",
			"address_line1": "Jl. Asia Afrika No. 20",
			"city": "Bandung",
		},
		{
			"salutation": "Mr",
			"first_name": "Nurul",
			"last_name": "Hidayat",
			"email": "nurul.hidayat@email.com",
			"phone": "+6281234567904",
			"company_name": "PT Kreatif Solusi",
			"gender": "Male",
			"address_line1": "Jl. Gajah Mada No. 11",
			"city": "Jakarta Barat",
		},
	]

	created = 0
	skipped = 0

	for data in contacts_data:
		# Check if contact already exists
		existing = frappe.db.exists("Contact Email", {"email_id": data["email"]})
		if existing:
			print(f"SKIPPED (email exists): {data['first_name']} {data['last_name']}")
			skipped += 1
			continue

		# Create Address document first
		address_title = f"{data['first_name']} {data['last_name']}"
		address = frappe.new_doc("Address")
		address.address_title = address_title
		address.address_type = "Billing"
		address.address_line1 = data["address_line1"]
		address.city = data["city"]
		address.country = "Indonesia"
		address.insert(ignore_permissions=True)

		# Create Contact
		contact = frappe.new_doc("Contact")
		contact.salutation = data["salutation"]
		contact.first_name = data["first_name"]
		contact.last_name = data["last_name"]
		contact.company_name = data["company_name"]
		contact.gender = data["gender"]
		contact.address = address.name

		# Add email to child table
		contact.append("email_ids", {
			"email_id": data["email"],
			"is_primary": 1,
		})

		# Add phone to child table
		contact.append("phone_nos", {
			"phone": data["phone"],
			"is_primary_mobile_no": 1,
		})

		contact.insert(ignore_permissions=True)
		print(f"CREATED: {data['first_name']} {data['last_name']} | email={contact.email_id} | phone={contact.mobile_no} | address={contact.address}")
		created += 1

	frappe.db.commit()
	print(f"\nDone! Created: {created}, Skipped: {skipped}")
