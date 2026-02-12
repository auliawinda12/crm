"""
Script untuk update email Administrator melalui command line.

Cara penggunaan:
    docker exec crm-frappe-1 bench --site crm.localhost execute update_admin_email_gui.update_admin_email --args 'new_email@example.com'
"""

import frappe
import getpass


def update_admin_email(new_email):
    """
    Update email address for Administrator user.

    Args:
        new_email (str): New email address for Administrator

    Returns:
        dict: Success status and message
    """

    print("=" * 60)
    print("UPDATE ADMINISTRATOR EMAIL")
    print("=" * 60)

    # Get current email
    current_email = frappe.db.get_value("User", "Administrator", "email")
    print(f"\n[1] Current Administrator Email: {current_email}")

    # Validate new email
    if not new_email or "@" not in new_email:
        return {
            "success": False,
            "message": "Invalid email address format"
        }

    # Check if email already exists for another user
    existing_user = frappe.db.get_value(
        "User",
        {"email": new_email, "name": ["!=", "Administrator"]},
        "name"
    )

    if existing_user:
        print(f"\n   Error: Email '{new_email}' is already in use by user '{existing_user}'")
        return {
            "success": False,
            "message": "Email already in use"
        }

    # Update Administrator email
    print(f"\n[2] Updating to: {new_email}")

    try:
        frappe.db.set_value("User", "Administrator", {
            "email": new_email,
            "username": new_email
        })
        frappe.db.commit()

        print(f"\n   Successfully updated Administrator email!")
        print(f"   Old email: {current_email}")
        print(f"   New email: {new_email}")

        return {
            "success": True,
            "message": f"Email updated to {new_email}"
        }

    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e)
        print(f"\n   Error: {error_msg}")

        return {
            "success": False,
            "message": f"Failed to update email: {error_msg}"
        }


def commands():
    """Register command for frappe bench"""
    return {
        "update_admin_email": update_admin_email
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python update_admin_email_gui.py <new_email>")
        print("Example: python update_admin_email_gui.py admin@example.com")
        sys.exit(1)

    new_email_arg = sys.argv[1]

    frappe.init(site="crm.localhost", sites_path="sites")
    frappe.connect()

    try:
        result = update_admin_email(new_email_arg)

        print("\n" + "=" * 60)
        if result["success"]:
            print("STATUS: SUCCESS")
            print(f"MESSAGE: {result['message']}")
        else:
            print("STATUS: FAILED")
            print(f"MESSAGE: {result['message']}")
        print("=" * 60)

        sys.exit(0 if result["success"] else 1)

    finally:
        frappe.destroy()
