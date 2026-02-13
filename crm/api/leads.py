# -*- coding: utf-8 -*-
import frappe
from frappe import _
from frappe.query_builder import DocType, Order
from frappe.database.query import functions
from pypika import Criterion
from frappe.desk.form.sorting import sort_order

@frappe.whitelist()
def get_leads_with_assignment_filter(start=0, page_length=20, preference=None, ignore_permissions=False):
    """
    Get leads with filter: Hide leads that have incoming emails but no assigned_to.

    This filters out leads where:
    - There are incoming email communications
    - AND all those communications have NULL assigned_to

    Args:
        start: Start index for pagination
        page_length: Number of records per page
        preference: User preference for filters
        ignore_permissions: Whether to ignore permissions

    Returns:
        dict: Lead data with filtered results
    """
    doctype = "CRM Lead"
    user = frappe.session.user

    # Base query - get leads that are not converted
    query = (
        frappe.qb.DocType(doctype)
        .field("status")
        .not_in(["Converted", "Lost", "Closed"])
    )

    # Apply permissions check if not ignoring
    if not ignore_permissions:
        query = (
            frappe.qb.user_permission_exists("CRM Lead", "read")
            .where(query)
        )

    # Add order by creation date (newest first)
    query = query.orderby("creation", order=Order.desc)

    # Execute query to get total count before pagination
    lead_query = query

    # Get total count before pagination
    leads = frappe.db.get_list(
        doctype,
        fields=["name", "lead_name", "email", "status", "company_name", "mobile_no", "owner", "creation"],
        filters=[["status", "not in", ["Converted", "Lost", "Closed"]],
        order_by="creation",
        order="desc",
        start=start,
        page_length=page_length
    )

    # Filter leads based on incoming emails and assigned_to
    filtered_leads = []
    for lead in leads:
        lead_name = lead.get("name")

        # Check if lead has incoming communications
        # Communications with reference_doctype = "CRM Lead" and reference_name = current lead
        communications = frappe.db.get_list(
            "Communication",
            filters={
                "reference_doctype": "CRM Lead",
                "reference_name": lead_name,
                "communication_type": "Communication",  # Only incoming communications
                "sent_or_received": "Received"
            },
            fields=["name", "sender", "subject", "creation"]
        )

        # Filter: Check if there are incoming communications without assigned_to
        unassigned_incoming = False
        has_incoming = False

        for comm in communications:
            has_incoming = True
            # Check if assigned_to is null or empty
            assigned_to = frappe.db.get_value("Communication", comm.get("name"), "assigned_to")

            if not assigned_to or assigned_to == "":
                unassigned_incoming = True
                break

        # Only exclude lead if:
        # 1. Has incoming communications
        # 2. AND all of those communications have NO assigned_to
        if has_incoming and unassigned_incoming:
            # Don't add this lead to filtered results
            continue

        # Lead passes filter - add to results
        filtered_leads.append(lead)

    return {
        "data": filtered_leads,
        "total_count": len(filtered_leads)
    }
