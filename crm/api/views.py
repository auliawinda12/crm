# -*- coding: utf-8 -*-
import frappe

@frappe.whitelist()
def get_views(doctype=None):
    """
    Get views for a specific doctype, with optional filter to exclude leads with unassigned incoming emails.

    Args:
        doctype (str): The doctype to get views for (e.g., CRM Lead)

    Returns:
        list: List of views for the doctype
    """
    # Get CRM View Settings
    View = frappe.qb.DocType("CRM View Settings")
    query = (
        frappe.qb.from_(View)
        .select("*")
        .where(
            (View.user == "") | (View.user == frappe.session.user)
        )
    )

    views = []

    if doctype:
        query = query.where(View.dt == doctype)
        views = query.run(as_dict=True)

        # Filter out views for leads if the filter setting is enabled
        if doctype == "CRM Lead" and frappe.db.exists("System Settings", {"name": "Hide Unassigned Email Leads"}):
            # Check if the filter to hide unassigned email leads is enabled
            hide_unassigned = frappe.db.get_value("System Settings", "Hide Unassigned Email Leads", "value")

            if hide_unassigned:
                # Get user preference for this filter
                user_preference = frappe.db.get_value("User", frappe.session.user, "hide_unassigned_email_leads", cache=False)
                if user_preference in [1, "1", True, "true", "True"]:
                    # Filter views to exclude the one that shows all leads
                    # Keep only custom views that have filters applied
                    views = [v for v in views if v.get("name") not in ["all", "All", "recently_modified", "created_on"]]

        return views

    return views


@frappe.whitelist()
def set_unassigned_email_filter(enabled=1):
    """
    Enable or disable the filter to hide leads with unassigned incoming emails.

    Args:
        enabled (int): 1 to enable, 0 to disable

    Returns:
        dict: Success message
    """
    # Update system setting
    if frappe.db.exists("System Settings", {"name": "Hide Unassigned Email Leads"}):
        frappe.db.set_value("System Settings", "Hide Unassigned Email Leads", "value", enabled)
    else:
        frappe.db.get_doc({
            "doctype": "System Settings",
            "name": "Hide Unassigned Email Leads",
            "value": enabled
        }).insert()

    # Update user preference
    frappe.db.set_value("User", frappe.session.user, "hide_unassigned_email_leads", enabled)

    return {
        "success": True,
        "message": "Filter " + ("enabled" if enabled else "disabled")
    }


@frappe.whitelist()
def get_unassigned_email_leads_count():
    """
    Get count of leads with unassigned incoming emails.

    Returns:
        dict: Count of such leads
    """
    leads = frappe.db.get_list("CRM Lead", fields=["name"], filters=[["status", "not in", ["Converted", "Lost", "Closed"]]])

    unassigned_count = 0
    for lead in leads:
        lead_name = lead.get("name")

        # Check if lead has incoming communications
        communications = frappe.db.get_list(
            "Communication",
            filters={
                "reference_doctype": "CRM Lead",
                "reference_name": lead_name,
                "communication_type": "Communication",
                "sent_or_received": "Received"
            },
            fields=["name", "sender", "subject", "creation", "assigned_to"]
        )

        # Check if all incoming communications have no assigned_to
        has_unassigned_incoming = False
        for comm in communications:
            assigned_to = comm.get("assigned_to")
            if not assigned_to or assigned_to == "":
                has_unassigned_incoming = True
                break

        if has_unassigned_incoming:
            unassigned_count += 1

    return {
        "count": unassigned_count,
        "message": f"Found {unassigned_count} leads with unassigned incoming emails"
    }
