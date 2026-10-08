from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import get_url


class CalendarExportSettings(Document):
	def validate(self):
		feed_token = self.get_password("feed_token", raise_exception=False)
		if not feed_token:
			feed_token = frappe.generate_hash(length=32)
			self.feed_token = feed_token
		self.feed_url = f"{get_url()}/api/method/sut_calendar_export.api.calendar_feed?token={feed_token}"
