import re

import frappe

CRM_REFERENCE_PATTERN = re.compile(r"\(#([A-Za-z0-9-]+)\)")
CRM_REFERENCE_DOCTYPES = ("CRM Lead", "CRM Deal")


def _extract_reference_from_subject(subject: str | None) -> tuple[str | None, str | None]:
	if not subject:
		return None, None

	for reference_name in CRM_REFERENCE_PATTERN.findall(subject):
		for doctype in CRM_REFERENCE_DOCTYPES:
			if frappe.db.exists(doctype, reference_name):
				return doctype, reference_name

	return None, None


def _link_communication_from_subject(doc) -> None:
	if doc.reference_doctype and doc.reference_name:
		return

	reference_doctype, reference_name = _extract_reference_from_subject(doc.subject)
	if not (reference_doctype and reference_name):
		return

	frappe.db.set_value(
		"Communication",
		doc.name,
		{
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
		},
		update_modified=False,
	)

	doc.reference_doctype = reference_doctype
	doc.reference_name = reference_name


def publish_communication_update(doc, method=None) -> None:
	if doc.doctype != "Communication":
		return

	if doc.communication_type != "Communication":
		return

	if doc.communication_medium != "Email":
		return

	# Incoming replies can arrive without linkage when append_to is Communication.
	# Link to CRM docs by subject token, e.g. "(#CRM-LEAD-2026-00001)".
	_link_communication_from_subject(doc)

	if doc.reference_doctype not in CRM_REFERENCE_DOCTYPES or not doc.reference_name:
		return

	frappe.publish_realtime(
		"crm_communication_update",
		{
			"communication": doc.name,
			"reference_doctype": doc.reference_doctype,
			"reference_name": doc.reference_name,
			"sent_or_received": doc.sent_or_received,
		},
		after_commit=True,
	)
