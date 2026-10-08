"""Public, token-protected endpoints for calendar consumers."""

from __future__ import annotations

import hmac

import frappe

from sut_calendar_export.ics import build_todo_calendar


@frappe.whitelist(allow_guest=True)
def calendar_feed(token: str | None = None):
	"""Return the current ERPNext ToDo calendar as an iCalendar feed.

	The token allows Outlook to read the feed without authenticating as an
	ERPNext user. It must therefore be treated like a password.
	"""
	settings = frappe.get_single("Calendar Export Settings")
	expected_token = settings.get_password("feed_token")

	if not settings.enabled or not token or not hmac.compare_digest(token, expected_token or ""):
		frappe.throw("Calendar feed not found.", frappe.DoesNotExistError)

	frappe.local.response.filename = "erpnext-todos.ics"
	frappe.local.response.filecontent = build_todo_calendar()
	frappe.local.response.type = "download"

