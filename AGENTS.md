# Instructions For AI Contributors

This repository contains the installable Frappe app `sut_calendar_export`.
Follow these rules for every change to this repository.

## Required Change Management

1. Update `sut_calendar_export/__init__.py` for every change. Increment the
   patch version by one, for example `0.0.1` to `0.0.2`.
2. Add an entry for that version to `CHANGELOG.md`. Describe the functional
   effect in concise user-facing language and include the current date.
3. Run the relevant tests before finishing. At minimum, run the ICS generator
   tests when changing feed generation, settings, or the API endpoint.
4. Keep the version change, changelog entry, implementation, and tests in the
   same commit.

Use semantic versioning: patch for compatible fixes or small additions, minor
for backwards-compatible features, and major for incompatible changes.

## Feed Contract

- The app provides a one-way, token-protected iCalendar feed for ERPNext ToDos.
- `Calendar Export Settings` is a singleton and must remain restricted to
  System Managers.
- Treat the feed URL and its token as secrets. Do not write them to logs,
  examples, tests, or documentation.
- The feed is generated on request; do not introduce background jobs or local
  calendar files unless explicitly required.
- ToDos without a due date cannot be represented as calendar events. Preserve
  this behavior unless a product decision specifies a date strategy.
