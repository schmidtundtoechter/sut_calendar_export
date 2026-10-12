"""iCalendar serialization for ERPNext ToDos."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from html import escape
from urllib.parse import quote

import frappe
from frappe.utils import get_datetime, get_url, slug, strip_html


def build_todo_calendar() -> str:
	"""Build an RFC 5545 calendar containing every ToDo with a due date."""
	link_fields = [
		field
		for field in frappe.get_meta("ToDo").fields
		if field.fieldtype in ("Link", "Dynamic Link")
		and field.fieldname
		not in ("reference_type", "allocated_to", "assigned_by", "role", "assignment_rule")
		and field.options
	]
	fields = [
		"name",
		"date",
		"description",
		"status",
		"priority",
		"allocated_to",
		"reference_type",
		"reference_name",
		"modified",
	]
	for field in link_fields:
		fields.append(field.fieldname)
		if field.fieldtype == "Dynamic Link":
			fields.append(field.options)
	todos = frappe.get_all(
		"ToDo",
		filters={"date": ["is", "set"]},
		fields=list(dict.fromkeys(fields)),
		order_by="date asc, modified desc",
	)
	for todo in todos:
		todo["linked_documents"] = [
			(
				field.options if field.fieldtype == "Link" else todo.get(field.options),
				todo.get(field.fieldname),
			)
			for field in link_fields
		]
	return build_calendar(todos, frappe.local.site, get_url())


def build_calendar(todos: list[dict], site_name: str, base_url: str | None = None) -> str:
	"""Serialize ToDo mappings as a portable all-day iCalendar feed."""
	lines = [
		"BEGIN:VCALENDAR",
		"VERSION:2.0",
		"PRODID:-//SUT GmbH//ERPNext ToDo Calendar Export//EN",
		"CALSCALE:GREGORIAN",
		"METHOD:PUBLISH",
		"X-WR-CALNAME:ERPNext ToDos",
	]

	for todo in todos:
		lines.extend(_todo_to_event(todo, site_name, base_url or f"https://{site_name}"))

	lines.append("END:VCALENDAR")
	return "\r\n".join(_fold_ical_line(line) for line in lines) + "\r\n"


def _todo_to_event(todo: dict, site_name: str, base_url: str) -> list[str]:
	due_date = _as_date(todo.get("date"))
	summary = _todo_summary(todo)
	description = _todo_description(todo, base_url)
	status = {"Closed": "COMPLETED", "Cancelled": "CANCELLED"}.get(todo.get("status"), "CONFIRMED")
	modified = get_datetime(todo.get("modified") or datetime.now())

	return [
		"BEGIN:VEVENT",
		f"UID:{_escape_ical(todo.get('name'))}@{_escape_ical(site_name)}",
		f"DTSTAMP:{modified.strftime('%Y%m%dT%H%M%SZ')}",
		f"LAST-MODIFIED:{modified.strftime('%Y%m%dT%H%M%SZ')}",
		f"DTSTART;VALUE=DATE:{due_date.strftime('%Y%m%d')}",
		f"DTEND;VALUE=DATE:{(due_date + timedelta(days=1)).strftime('%Y%m%d')}",
		f"SUMMARY:{_escape_ical(summary)}",
		f"DESCRIPTION:{_escape_ical(description)}",
		f"X-ALT-DESC;FMTTYPE=text/html:{_escape_ical(_description_html(description))}",
		f"STATUS:{status}",
		"CATEGORIES:ERPNext ToDo",
		"TRANSP:TRANSPARENT",
		"END:VEVENT",
	]


def _todo_summary(todo: dict) -> str:
	text = strip_html(todo.get("description") or "").strip()
	return text.splitlines()[0] if text else f"ToDo {todo.get('name')}"


def _todo_description(todo: dict, base_url: str) -> str:
	parts = [strip_html(todo.get("description") or "").strip()]
	if todo.get("priority"):
		parts.append(f"Priority: {todo.get('priority')}")
	if todo.get("allocated_to"):
		parts.append(f"Allocated to: {todo.get('allocated_to')}")
	documents = [("ToDo", todo.get("name")), (todo.get("reference_type"), todo.get("reference_name"))]
	documents.extend(todo.get("linked_documents") or [])
	seen = set()
	links = []
	for doctype, name in documents:
		if not doctype or not name or (doctype, name) in seen:
			continue
		seen.add((doctype, name))
		url = f"{base_url.rstrip('/')}/app/{quote(slug(doctype), safe='')}/{quote(str(name), safe='')}"
		links.append(f"Link zum {doctype} ({name}):\n{url}")
	return "\n\n".join(["\n".join(part for part in parts if part), *links]).strip()


def _description_html(description: str) -> str:
	"""Provide explicit hyperlinks for Outlook, with a plain-text fallback."""
	lines = []
	for line in description.split("\n"):
		text = escape(line)
		if line.startswith(("https://", "http://")):
			text = f'<a href="{text}">{text}</a>'
		lines.append(text)
	return "<html><body>" + "<br>".join(lines) + "</body></html>"


def _as_date(value) -> date:
	if isinstance(value, datetime):
		return value.date()
	if isinstance(value, date):
		return value
	return get_datetime(value).date()


def _escape_ical(value: str) -> str:
	return (
		str(value)
		.replace("\\", "\\\\")
		.replace(";", "\\;")
		.replace(",", "\\,")
		.replace("\r\n", "\\n")
		.replace("\n", "\\n")
	)


def _fold_ical_line(line: str) -> str:
	"""Fold long content lines as required by RFC 5545 (75 octets maximum)."""
	encoded = line.encode("utf-8")
	if len(encoded) <= 75:
		return line

	chunks = []
	current = ""
	for character in line:
		candidate = current + character
		if len(candidate.encode("utf-8")) > 75:
			chunks.append(current)
			current = " " + character
		else:
			current = candidate
	chunks.append(current)
	return "\r\n".join(chunks)
