# SUT Calendar Export

## Deutsch

SUT Calendar Export stellt ERPNext-ToDos als abonnierbaren Outlook-Kalender bereit. ERPNext liefert den Feed nur lesend aus: Outlook kann die Kalendereinträge anzeigen, Änderungen in Outlook werden jedoch nicht nach ERPNext zurückgeschrieben.

### Installation

~~~bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app sut_calendar_export
~~~

Eine einfache Anleitung für Anwender steht in [docs/kundenanleitung.md](docs/kundenanleitung.md).

### Funktionsweise

Der Feed ist eine dynamisch erzeugte iCalendar-Datei (.ics). Bei jedem Abruf liest ERPNext die aktuellen ToDos und liefert den Kalender neu aus. Es gibt keinen manuellen Dateiexport und keinen zeitgesteuerten ERPNext-Job. Wann eine Änderung in Outlook sichtbar wird, bestimmt Outlook beziehungsweise Microsoft durch den eigenen Aktualisierungsrhythmus.

Jedes ToDo mit einem Datum im Feld Date wird als ganztägiger Kalendereintrag exportiert. Beschreibung, Priorität, Zuweisung und gegebenenfalls eine ERPNext-Referenz werden übernommen. ToDos ohne Datum können technisch nicht als Kalendereintrag dargestellt werden und werden daher nicht exportiert.

### Einrichtung in ERPNext

1. Für jedes zu exportierende ToDo im Standard-DocType ToDo ein Datum im Feld Date hinterlegen.
2. Als Benutzer mit der Rolle System Manager nach Calendar Export Settings suchen und den DocType öffnen.
3. Enable Calendar Feed aktivieren und speichern. Beim ersten Speichern erzeugt die App die Outlook Feed URL.
4. In Outlook Kalender hinzufügen und anschließend Aus dem Internet abonnieren wählen. Die Outlook Feed URL einfügen und bestätigen.

Beteiligt sind die DocTypes ToDo als Datenquelle und Calendar Export Settings als zentrale, nur für System Manager verfügbare Konfiguration.

### Sicherheit

Die Outlook Feed URL enthält einen persönlichen Token und ist wie ein Passwort zu behandeln. Wer die URL kennt, kann die exportierten ToDo-Informationen lesen. Die URL darf daher nicht in Tickets, Screenshots, Quellcode oder öffentliche Dokumente gelangen. Wenn der Token geändert wird, wird die bisherige URL ungültig; das Outlook-Abonnement muss anschließend mit der neuen URL eingerichtet werden.

## English

SUT Calendar Export provides ERPNext ToDos as a subscribable Outlook calendar. ERPNext serves the feed as read-only: Outlook can display the calendar entries, but changes made in Outlook are not written back to ERPNext.

### Installation

~~~bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app sut_calendar_export
~~~

A simple German end-user guide is available at [docs/kundenanleitung.md](docs/kundenanleitung.md).

### How It Works

The feed is generated dynamically as an iCalendar (.ics) file. Whenever Outlook requests it, ERPNext reads the current ToDos and returns a fresh calendar. There is no manual file export and no scheduled ERPNext job. Outlook or Microsoft controls how quickly a change becomes visible in Outlook.

Each ToDo with a value in the Date field is exported as an all-day calendar entry. The description, priority, assignment, and an optional ERPNext reference are included. ToDos without a date cannot be represented as calendar events and are therefore not exported.

### ERPNext Setup

1. Add a value to the Date field on every standard ToDo that should be exported.
2. As a user with the System Manager role, open Calendar Export Settings.
3. Enable the calendar feed and save. The app generates the Outlook Feed URL on the first save.
4. In Outlook, choose Add calendar and then Subscribe from web. Paste the Outlook Feed URL and confirm the subscription.

The relevant DocTypes are ToDo as the source of calendar data and Calendar Export Settings as the central configuration, available only to System Managers.

### Security

The Outlook Feed URL contains a personal token and must be treated like a password. Anyone with the URL can read the exported ToDo information. Do not share it in tickets, screenshots, source code, or public documents. Changing the token invalidates the old URL, so the Outlook subscription must be updated with the new URL.

## Contributing

This app uses pre-commit for formatting and linting.

~~~bash
cd apps/sut_calendar_export
pre-commit install
~~~

## CI

- CI installs the app and runs unit tests on every push to the develop branch.
- Linters run Frappe Semgrep Rules and pip-audit on every pull request.

## License

MIT
