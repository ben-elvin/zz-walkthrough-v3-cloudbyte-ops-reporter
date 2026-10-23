# CloudByte Ops Reporter

A command-line tool that summarises CloudByte Solutions' operational activity.
Built across the Python chapter of the cloud bootcamp, one feature per section.

## Running it

```
python3 cloudbyte_report.py
python3 cloudbyte_report.py --user alice -v
```

It reads CloudByte's access log (`cloudbyte_access.log`) and prints an access report: a header
with the event total and time span, then one tidy line per event.

It now ranks users by how active they are, listing the most active first.

It now ranks three views, most active users, busiest hours, and activity by type, all through one shared function.

It now filters as well as ranks, with a login-activity view and a per-user breakdown built from list comprehensions.

It now reads the staff roster from users.csv and joins it to the log to report activity by department.

It now parses the upgraded log with a regular expression and reports the most requested paths and the failed requests, by department and by path.

It now runs from the command line: give it a log path to read, --user NAME for one person's breakdown, and -v for extra detail. A line it can't read is skipped and logged instead of stopping the run.

## Where it runs

The reporter now runs unattended every morning on a Linux server, started by cron.
Where it lives, what starts it and when, and how to check that the last run
produced a good report are all in [docs/deploy-notes.md](docs/deploy-notes.md).
