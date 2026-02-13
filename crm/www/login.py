import frappe
from frappe import _
from frappe.utils import get_url

def get_context(context):
    context.no_cache = 1
    if frappe.session.user != "Guest":
        frappe.local.flags.redirect_location = "/crm"
        raise frappe.Redirect
    
    # Pass app specific context
    context.app_title = frappe.get_hooks("app_title")[0]
    # Check if we have a custom logo in hooks, else fall back
    context.app_logo_url = frappe.get_hooks("app_icon_url")[0]
    context.year = frappe.utils.now_datetime().year
    
    return context
