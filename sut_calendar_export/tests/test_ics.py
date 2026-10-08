from datetime import datetime

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
