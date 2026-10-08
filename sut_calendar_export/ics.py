"""iCalendar serialization for ERPNext ToDos."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

import frappe
from frappe.utils import get_datetime, strip_html


def build_todo_calendar() -> str:
	"""Build an RFC 5545 calendar containing every ToDo with a due date."""
	todos = frappe.get_all(
		"ToDo",
		filters={"date": ["is", "set"]},
		fields=["name", "date", "description", "status", "priority", "allocated_to", "reference_type", "reference_name", "modified"],
		order_by="date asc, modified desc",
	)
	return build_calendar(todos, frappe.local.site)


def build_calendar(todos: list[dict], site_name: str) -> str:
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
		lines.extend(_todo_to_event(todo, site_name))

	lines.append("END:VCALENDAR")
	return "\r\n".join(_fold_ical_line(line) for line in lines) + "\r\n"


def _todo_to_event(todo: dict, site_name: str) -> list[str]:
	due_date = _as_date(todo.get("date"))
	summary = _todo_summary(todo)
	description = _todo_description(todo)
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
		f"STATUS:{status}",
		"CATEGORIES:ERPNext ToDo",
		"TRANSP:TRANSPARENT",
		"END:VEVENT",
	]


def _todo_summary(todo: dict) -> str:
	text = strip_html(todo.get("description") or "").strip()
	return text.splitlines()[0] if text else f"ToDo {todo.get('name')}"


def _todo_description(todo: dict) -> str:
	parts = [strip_html(todo.get("description") or "").strip()]
	if todo.get("priority"):
		parts.append(f"Priority: {todo.get('priority')}")
	if todo.get("allocated_to"):
		parts.append(f"Allocated to: {todo.get('allocated_to')}")
	if todo.get("reference_type") and todo.get("reference_name"):
		parts.append(f"Reference: {todo.get('reference_type')} {todo.get('reference_name')}")
	return "\n".join(part for part in parts if part)


def _as_date(value) -> date:
	if isinstance(value, datetime):
		return value.date()
	if isinstance(value, date):
		return value
	return get_datetime(value).date()


def _escape_ical(value: str) -> str:
	return str(value).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\r\n", "\\n").replace("\n", "\\n")


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
