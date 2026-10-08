### SUT Calendar Export

`sut_calendar_export` stellt ERPNext-ToDos als abonnierten Outlook-Kalender
bereit. ERPNext ist dabei die lesende Quelle des Feeds: Outlook kann die
Kalendereintraege anzeigen, aber keine Aenderungen nach ERPNext zurueckschreiben.
Der Outlook-Kalender bleibt damit das datenfuehrende System fuer seine eigenen
Kalendereintraege.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app sut_calendar_export
```

Eine einfache deutsche Anleitung fuer Anwender steht in
[docs/kundenanleitung.md](docs/kundenanleitung.md).

### Funktionsweise

Der Feed ist eine dynamisch erzeugte iCalendar-Datei (`.ics`). Bei jedem Abruf
liest ERPNext die aktuellen ToDos und liefert den Kalender sofort neu aus. Es
gibt daher keinen Dateiexport und keinen zeitgesteuerten ERPNext-Job, der
veralten kann. Wie schnell eine Aenderung in Outlook sichtbar wird, bestimmt
Outlook beziehungsweise Microsoft durch den eigenen Aktualisierungsrhythmus;
ERPNext stellt beim naechsten Abruf stets den aktuellen Stand bereit.

Jedes ToDo mit einem gesetzten Faelligkeitsdatum erscheint als ganztagiger
Kalendereintrag. Exportiert werden Beschreibung, Prioritaet, Zuweisung und
optional die verknuepfte ERPNext-Referenz. Abgeschlossene und stornierte ToDos
werden mit dem passenden Kalenderstatus uebertragen. ToDos ohne
Faelligkeitsdatum koennen technisch nicht als Kalendereintrag dargestellt
werden und werden deshalb nicht exportiert.

### Einrichtung In ERPNext

1. Stelle sicher, dass jedes zu exportierende **ToDo** im Standard-DocType
   `ToDo` ein Faelligkeitsdatum im Feld `Date` besitzt.
2. Melde dich als Benutzer mit der Rolle **System Manager** an und oeffne den
   Singleton-DocType **Calendar Export Settings**.
3. Aktiviere **Enable Calendar Feed** und speichere. Beim ersten Speichern
   erzeugt die App einen individuellen Token und die **Outlook Feed URL**.
4. Kopiere die angezeigte URL in Outlook ueber "Kalender hinzufuegen" und
   anschliessend "Aus dem Internet abonnieren" (die genaue Bezeichnung kann je
   nach Outlook-Version abweichen).

Folgende DocTypes sind beteiligt:

- `ToDo`: Quelle aller exportierten Aufgaben; das Feld `Date` entscheidet, ob
  ein Kalendereintrag erzeugt werden kann.
- `Calendar Export Settings`: App-Einstellungen pro ERPNext-Site. Hier werden
  Aktivierung, die abonnierbare URL und der Token verwaltet. Dieser DocType ist
  ausschliesslich fuer System Manager vorgesehen.

### Sicherheit Des Feed-Tokens

Die Feed-URL enthaelt einen zufaelligen Token und ist damit wie ein Passwort zu
behandeln. Wer die URL kennt, kann alle exportierten ToDo-Informationen lesen.
Teile sie deshalb nur mit dem vorgesehenen Outlook-Konto und hinterlege sie
nicht in Tickets, Screenshots, Quellcode oder oeffentlichen Dokumenten.

Wird der Token in **Calendar Export Settings** geaendert, ist die alte URL
ungueltig. Aktualisiere dann auch das Outlook-Abonnement mit der neu erzeugten
URL.

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/sut_calendar_export
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
