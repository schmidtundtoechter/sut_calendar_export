### SUT Calendar Export

Outlook calendar feeds for ERPNext ToDos

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app sut_calendar_export
```

### Outlook Feed

After installing the app, open **Calendar Export Settings** as a System Manager
and copy the generated **Outlook Feed URL** into Outlook's "Subscribe from web"
dialog. The endpoint generates an up-to-date iCalendar (`.ics`) feed for every
ToDo with a due date. It is intentionally one-way: changes in Outlook are not
written back to ERPNext.

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
