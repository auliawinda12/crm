"""
Test script untuk menguji pengiriman email ke Lead.
Script ini akan mengirim email test ke lead yang ada di sistem.

Cara penggunaan dengan Docker:
    docker exec crm-frappe-1 bash -c 'cd /home/frappe/frappe-bench && ./env/bin/python /tmp/test_lead.py'
"""

import frappe


def get_leads(limit=10):
    """Mengambil daftar lead yang ada"""
    print(f"\n[Mengambil {limit} lead terbaru...]")

    leads = frappe.db.get_all(
        "CRM Lead",
        fields=["name", "lead_name", "email", "mobile_no", "status"],
        filters={"status": ["!=", "Converted"]},
        order_by="creation desc",
        limit=limit
    )

    if leads:
        print(f"   Ditemukan {len(leads)} lead:")
        for i, lead in enumerate(leads, 1):
            email = lead.get('email') or 'Tidak ada email'
            print(f"      {i}. {lead.get('name')} - {lead.get('lead_name')} ({email})")
    else:
        print("   Tidak ada lead ditemukan")

    return leads


def test_email_to_lead(lead_name, lead_email, lead_display_name):
    """Test pengiriman email ke lead tertentu"""

    print(f"\n[TEST] Mengirim email ke Lead: {lead_display_name}")
    print(f"       Email tujuan: {lead_email}")

    # Cek Default Outgoing Email Account
    default_email_account = frappe.db.get_value(
        "Email Account",
        {"default_outgoing": 1, "enable_outgoing": 1},
        ["name", "email_id", "smtp_server"],
        as_dict=True
    )

    if default_email_account:
        print(f"   ✅ Menggunakan Default Outgoing: {default_email_account.get('email_id')}")
    else:
        print("   ⚠️  Default Outgoing belum diset - akan menggunakan Administrator")

    # Create communication document directly
    try:
        comm = frappe.get_doc({
            "doctype": "Communication",
            "reference_doctype": "CRM Lead",
            "reference_name": lead_name,
            "subject": "Test Email dari CRM - Follow Up",
            "content": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #007bff; color: white; padding: 20px; text-align: center;">
                    <h2 style="margin: 0;">Test Email CRM</h2>
                </div>
                <div style="padding: 20px; background-color: #f8f9fa;">
                    <p>Halo <strong>{lead_display_name}</strong>,</p>
                    <p>Ini adalah email test untuk memverifikasi pengiriman email ke lead.</p>
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📧 Subject:</strong> Test Email</p>
                        <p style="margin: 5px 0;"><strong>👤 Purpose:</strong> Test pengiriman email ke Lead</p>
                    </div>
                    <p style="color: #666; font-size: 12px;">Jika Anda menerima email ini, berarti konfigurasi email sudah benar.</p>
                    <p style="margin-top: 20px;">Salam,</p>
                    <p><strong>Tim CRM</strong></p>
                </div>
            </div>
            """,
            "sent_or_received": "Sent",
            "communication_medium": "Email",
            "recipients": lead_email,
        })

        print("   Menyimpan Communication...")
        comm.insert(ignore_permissions=True)
        frappe.db.commit()

        print(f"   ✅ Communication created: {comm.name}")
        print(f"      Status: {comm.status}")

        print("   Mengirim email...")
        comm.send_email()
        frappe.db.commit()

        print("   ✅ Email berhasil dikirim!")
        print(f"      Communication Name: {comm.name}")
        print(f"      Status: {comm.status}")
        print(f"      Recipient: {lead_email}")
        return True

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_communications(lead_name, limit=5):
    """Cek communication history untuk lead tertentu"""
    print(f"\n[Cek History Communication untuk Lead: {lead_name}]")

    communications = frappe.db.get_all(
        "Communication",
        fields=["name", "subject", "sender", "recipient", "status", "creation"],
        filters={
            "reference_doctype": "CRM Lead",
            "reference_name": lead_name
        },
        order_by="creation desc",
        limit=limit
    )

    if communications:
        print(f"   Ditemukan {len(communications)} communication:")
        for comm in communications:
            print(f"      - {comm.get('name')} | {comm.get('subject')}")
            print(f"        From: {comm.get('sender')} | To: {comm.get('recipient')}")
            print(f"        Status: {comm.get('status')} | Created: {comm.get('creation')}")
    else:
        print("   Tidak ada communication ditemukan")


def interactive_test():
    """Mode interaktif untuk memilih lead"""
    print("=" * 70)
    print("TEST PENGIRIMAN EMAIL KE LEAD")
    print("=" * 70)

    # Ambil daftar lead
    leads = get_leads(limit=20)

    if not leads:
        print("\n❌ Tidak ada lead yang bisa diuji!")
        print("   Silakan buat lead terlebih dahulu.")
        return False

    # Filter lead yang punya email
    leads_with_email = [l for l in leads if l.get('email')]

    if not leads_with_email:
        print("\n❌ Tidak ada lead yang memiliki alamat email!")
        print("   Silakan tambahkan email pada lead terlebih dahulu.")
        return False

    # Kirim email ke lead pertama yang punya email (untuk test otomatis)
    # Bisa dimodifikasi untuk memilih lead tertentu
    target_lead = leads_with_email[0]

    print(f"\n{'=' * 70}")
    print(f"Target Lead: {target_lead.get('lead_name')} ({target_lead.get('email')})")
    print(f"{'=' * 70}")

    # Kirim email
    success = test_email_to_lead(
        target_lead.get('name'),
        target_lead.get('email'),
        target_lead.get('lead_name')
    )

    # Cek communication history
    check_communications(target_lead.get('name'))

    # Cek email queue
    print("\n[Cek Email Queue Terbaru]")
    email_queue = frappe.db.get_all(
        "Email Queue",
        fields=["name", "status", "creation"],
        order_by="creation desc",
        limit=5
    )

    if email_queue:
        print(f"   Ditemukan {len(email_queue)} email di queue:")
        for q in email_queue:
            print(f"      - {q.get('name')} | Status: {q.get('status')}")
    else:
        print("   Tidak ada email di queue")

    print("\n" + "=" * 70)
    if success:
        print("✅ TEST BERHASIL - Email berhasil dikirim ke Lead!")
        print(f"\nSilakan cek email inbox di: {target_lead.get('email')}")
    else:
        print("❌ TEST GAGAL - Silakan cek error di atas")
    print("=" * 70)

    return success


def test_specific_lead(lead_id):
    """Test ke lead tertentu berdasarkan ID/Nama"""
    print("=" * 70)
    print("TEST PENGIRIMAN EMAIL KE LEAD SPECIFIC")
    print("=" * 70)

    # Get lead data
    lead = frappe.db.get_value(
        "CRM Lead",
        lead_id,
        ["name", "lead_name", "email", "mobile_no", "status"],
        as_dict=True
    )

    if not lead:
        print(f"\n❌ Lead dengan ID '{lead_id}' tidak ditemukan!")
        return False

    if not lead.get('email'):
        print(f"\n❌ Lead '{lead.get('lead_name')}' tidak memiliki email!")
        return False

    print(f"\nTarget Lead: {lead.get('lead_name')} ({lead.get('email')})")

    # Kirim email
    success = test_email_to_lead(lead.get('name'), lead.get('email'), lead.get('lead_name'))

    # Cek communication history
    check_communications(lead.get('name'))

    print("\n" + "=" * 70)
    if success:
        print("✅ TEST BERHASIL!")
    else:
        print("❌ TEST GAGAL!")
    print("=" * 70)

    return success


if __name__ == "__main__":
    import sys

    try:
        # Initialize frappe
        frappe.init(site="localhost")
        frappe.connect()

        # Cek apakah ada argument untuk lead ID tertentu
        if len(sys.argv) > 1:
            lead_id = sys.argv[1]
            success = test_specific_lead(lead_id)
        else:
            # Jalankan test interaktif
            success = interactive_test()

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        frappe.destroy()
