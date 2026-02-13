# -*- coding: utf-8 -*-
import frappe

frappe.init(site="crm.localhost")
frappe.connect()

try:
    # Email Template 1: Welcome
    doc1 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Welcome Email Indonesia",
        "subject": "Selamat Datang di {{ doc.lead_name or 'Kami' }}!",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Selamat Datang! 👋</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Terima kasih telah bergabung dengan kami. Kami sangat senang bisa terhubung dengan Anda!</p>
<br>
<p>Salam hangat,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Welcome Email Indonesia"):
        doc1.insert()
        print("Created: Welcome Email Indonesia")
    else:
        print("Updated: Welcome Email Indonesia")

    # Email Template 2: Follow Up
    doc2 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Follow Up Email Indonesia",
        "subject": "Mengikuti Permintaan Anda",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Halo {{ doc.lead_name or 'Teman' }}! 👋</h2>
<p>Saya ingin mengikuti pesan saya sebelumnya mengenai produk/jasa kami.</p>
<p>Apakah Anda sudah memiliki waktu untuk mempertimbangkan tawaran kami?</p>
<br>
<p>Terima kasih atas waktu Anda,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Follow Up Email Indonesia"):
        doc2.insert()
        print("Created: Follow Up Email Indonesia")
    else:
        print("Updated: Follow Up Email Indonesia")

    # Email Template 3: Thank You
    doc3 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Thank You Email Indonesia",
        "subject": "Terima Kasih atas Waktu Anda!",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Terima Kasih! 🙏</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Terima kasih telah meluangkan waktu untuk berbicara dengan kami.</p>
<br>
<p>Salam hangat,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Thank You Email Indonesia"):
        doc3.insert()
        print("Created: Thank You Email Indonesia")
    else:
        print("Updated: Thank You Email Indonesia")

    # Email Template 4: Meeting Invitation
    doc4 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Meeting Invitation Email Indonesia",
        "subject": "Undangan Meeting",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Undangan Meeting 📅</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Kami ingin mengundang Anda untuk meeting guna membahas peluang kerjasama lebih lanjut.</p>
<br>
<p>Terima kasih,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Meeting Invitation Email Indonesia"):
        doc4.insert()
        print("Created: Meeting Invitation Email Indonesia")
    else:
        print("Updated: Meeting Invitation Email Indonesia")

    # Email Template 5: Quotation
    doc5 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Quotation Email Indonesia",
        "subject": "Quotation untuk Anda",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Quotation / Penawaran Harga 📄</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Terima kasih telah minat dengan produk/jasa kami.</p>
<p>Berikut adalah quotation untuk permintaan Anda:</p>
<div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
<p><strong>No. Quotation:</strong> {{ doc.quotation_number or 'QT-001' }}</p>
<p><strong>Tanggal Berlaku:</strong> {{ doc.valid_until or '14 Hari' }}</p>
<p><strong>Total:</strong> {{ doc.total_amount or 'Segera diinfokan' }}</p>
</div>
<br>
<p>Terima kasih,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Quotation Email Indonesia"):
        doc5.insert()
        print("Created: Quotation Email Indonesia")
    else:
        print("Updated: Quotation Email Indonesia")

    # Email Template 6: Payment Reminder
    doc6 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Payment Reminder Email Indonesia",
        "subject": "Pengingat Pembayaran",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #e74c3c;">Pengingat Pembayaran 💳</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Ini adalah pengingat untuk pembayaran invoice yang belum terselesaikan.</p>
<div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
<p><strong>No. Invoice:</strong> {{ doc.invoice_number or 'INV-001' }}</p>
<p><strong>Jatuh Tempo:</strong> {{ doc.due_date or 'Segera diinfokan' }}</p>
<p><strong>Jumlah:</strong> {{ doc.amount or 'Segera diinfokan' }}</p>
</div>
<br>
<p>Terima kasih,</p>
<p><strong>Tim Keuangan</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Payment Reminder Email Indonesia"):
        doc6.insert()
        print("Created: Payment Reminder Email Indonesia")
    else:
        print("Updated: Payment Reminder Email Indonesia")

    # Email Template 7: Support Ticket
    doc7 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Support Ticket Indonesia",
        "subject": "Tiket Dibuat",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #2c3e50;">Tiket Support Dibuat ✅</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Terima kasih telah menghubungi tim support kami.</p>
<p>Tiket Anda telah berhasil dibuat. Tim kami akan segera menindaklanjuti permintaan Anda.</p>
<br>
<p>Terima kasih atas kesabaran Anda,</p>
<p><strong>Tim Support</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Support Ticket Indonesia"):
        doc7.insert()
        print("Created: Support Ticket Indonesia")
    else:
        print("Updated: Support Ticket Indonesia")

    # Email Template 8: Promotional
    doc8 = frappe.get_doc({
        "doctype": "Email Template",
        "name": "Promotional Email Indonesia",
        "subject": "Penawaran Spesial untuk Anda! 🎉",
        "response_html": """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h2 style="color: #e74c3c;">Penawaran Spesial! 🎉</h2>
<p>Halo <strong>{{ doc.lead_name or 'Teman' }}</strong>,</p>
<p>Kami memiliki penawaran spesial untuk Anda!</p>
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin: 20px 0; text-align: center;">
<h3 style="color: white; margin-top: 0;">20% DISKON</h3>
<p style="font-size: 18px; margin: 10px 0;">Penawaran Terbatas!</p>
<p style="font-size: 14px;">Gunakan kode: PROMO20</p>
</div>
<br>
<p>Terima kasih,</p>
<p><strong>Tim Kami</strong></p>
</div>""",
        "enabled": 1,
        "use_html": 1,
    })
    if not frappe.db.exists("Email Template", "Promotional Email Indonesia"):
        doc8.insert()
        print("Created: Promotional Email Indonesia")
    else:
        print("Updated: Promotional Email Indonesia")

    print("\n=== SUMMARY ===")
    print("8 Indonesian Email Templates created/updated!")

except Exception as e:
    print("Error: " + str(e))
    import traceback
    traceback.print_exc()
finally:
    frappe.destroy()
