from datetime import datetime
from types import SimpleNamespace

from sut_calendar_export import ics
from sut_calendar_export.ics import build_calendar


def test_build_calendar_serializes_todo_as_all_day_event():
	calendar = build_calendar(
		[
			{
				"name": "TODO-0001",
				"date": "2026-10-08",
				"description": "Call ACME, Inc.; confirm next steps",
				"status": "Open",
				"priority": "High",
				"allocated_to": "sales@example.com",
				"reference_type": "Customer",
				"reference_name": "ACME",
				"modified": datetime(2026, 10, 7, 10, 30),
			}
		],
		"d-code.localhost",
	)

	assert "BEGIN:VCALENDAR" in calendar
	assert "UID:TODO-0001@d-code.localhost" in calendar
	assert "DTSTART;VALUE=DATE:20261008" in calendar
	assert "DTEND;VALUE=DATE:20261009" in calendar
	assert "SUMMARY:Call ACME\\, Inc.\\; confirm next steps" in calendar
	assert "STATUS:CONFIRMED" in calendar


def test_build_calendar_maps_closed_todos_to_completed_events():
	calendar = build_calendar(
		[
			{
				"name": "TODO-0002",
				"date": "2026-10-08",
				"description": "Finished",
				"status": "Closed",
				"priority": None,
				"allocated_to": None,
				"reference_type": None,
				"reference_name": None,
				"modified": datetime(2026, 10, 7, 10, 30),
			}
		],
		"d-code.localhost",
	)

	assert "STATUS:COMPLETED" in calendar


def test_description_links_are_separated_encoded_and_deduplicated():
	calendar = build_calendar(
		[
			{
				"name": "TODO-0003",
				"date": "2026-10-26",
				"description": "Follow up",
				"reference_type": "Quotation",
				"reference_name": "QTN/2026 #1",
				"linked_documents": [
					("Quotation", "QTN/2026 #1"),
					("Contact", "Müller & Sohn"),
					("Address", "Office"),
					("Contact", None),
					(None, "unused"),
				],
			}
		],
		"erp.example.com",
		"https://erp.example.com:8443/",
	).replace("\r\n ", "")
	description = next(line for line in calendar.split("\r\n") if line.startswith("DESCRIPTION:"))
	assert (
		"Follow up\\n\\nLink zum ToDo (TODO-0003):\\nhttps://erp.example.com:8443/app/todo/TODO-0003"
		in description
	)
	assert (
		"\\n\\nLink zum Quotation (QTN/2026 #1):\\nhttps://erp.example.com:8443/app/quotation/QTN%2F2026%20%231"
		in description
	)
	assert (
		"\\n\\nLink zum Contact (Müller & Sohn):\\nhttps://erp.example.com:8443/app/contact/M%C3%BCller%20%26%20Sohn"
		in description
	)
	assert "\\n\\nLink zum Address (Office):\\nhttps://erp.example.com:8443/app/address/Office" in description
	assert description.count("Link zum Quotation") == 1
	assert "unused" not in description
	assert "X-ALT-DESC;FMTTYPE=text/html:" in calendar
	assert '<a href="https://erp.example.com:8443/app/todo/TODO-0003">' in calendar
	assert r"<br><br>Link zum Contact (Müller &amp\; Sohn)" in calendar


def test_feed_collects_direct_custom_links_and_uses_site_url(monkeypatch):
	fields = [
		SimpleNamespace(fieldname="reference_type", fieldtype="Link", options="DocType"),
		SimpleNamespace(fieldname="reference_name", fieldtype="Dynamic Link", options="reference_type"),
		SimpleNamespace(fieldname="allocated_to", fieldtype="Link", options="User"),
		SimpleNamespace(fieldname="custom_contact", fieldtype="Link", options="Contact"),
		SimpleNamespace(fieldname="custom_record", fieldtype="Dynamic Link", options="custom_type"),
	]
	monkeypatch.setattr(ics.frappe, "get_meta", lambda doctype: SimpleNamespace(fields=fields))
	monkeypatch.setattr(ics.frappe, "local", SimpleNamespace(site="test.localhost"))
	monkeypatch.setattr(ics, "get_url", lambda: "http://test.localhost:8000")

	def get_all(doctype, **kwargs):
		assert doctype == "ToDo"
		assert kwargs["filters"] == {"date": ["is", "set"]}
		assert {"custom_contact", "custom_record", "custom_type"} <= set(kwargs["fields"])
		return [
			{
				"name": "TODO-0004",
				"date": "2026-10-26",
				"description": "Follow up",
				"reference_type": "Lead",
				"reference_name": "LEAD-001",
				"allocated_to": "sales@example.com",
				"custom_contact": "CONTACT-001",
				"custom_type": "Address",
				"custom_record": "ADDRESS-001",
			}
		]

	monkeypatch.setattr(ics.frappe, "get_all", get_all)
	calendar = ics.build_todo_calendar().replace("\r\n ", "")
	assert "http://test.localhost:8000/app/todo/TODO-0004" in calendar
	assert "http://test.localhost:8000/app/lead/LEAD-001" in calendar
	assert "http://test.localhost:8000/app/contact/CONTACT-001" in calendar
	assert "http://test.localhost:8000/app/address/ADDRESS-001" in calendar
	assert "/app/user/" not in calendar


def test_calendar_folds_unicode_links_within_75_octets():
	calendar = build_calendar(
		[{"name": "TODO-0005", "date": "2026-10-26", "description": "Ä" * 100}],
		"erp.example.com",
		"https://erp.example.com",
	)
	assert all(len(line.encode("utf-8")) <= 75 for line in calendar.split("\r\n"))
