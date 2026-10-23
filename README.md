# CloudByte Ops Reporter

A command-line tool that summarises CloudByte Solutions' operational activity.
Built across the Python chapter of the cloud bootcamp, one feature per section.

## Running it

```
python3 cloudbyte_report.py
```

It reads CloudByte's access log (`cloudbyte_access.log`) and prints an access report: a header
with the event total and time span, then one tidy line per event.

It now ranks users by how active they are, listing the most active first.

It now ranks three views, most active users, busiest hours, and activity by type, all through one shared function.

It now filters as well as ranks, with a login-activity view and a per-user breakdown built from list comprehensions.

It now reads the staff roster from users.csv and joins it to the log to report activity by department.

## What's coming

Future versions will read CloudByte's staff roster to report activity per person and per
department.
