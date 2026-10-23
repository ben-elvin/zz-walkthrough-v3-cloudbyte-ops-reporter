# CloudByte Ops Reporter

A command-line tool that summarises CloudByte Solutions' operational activity.
Built across the Python chapter of the cloud bootcamp, one feature per section.

## Running it

```
python3 cloudbyte_report.py
```

It reads CloudByte's access log (`cloudbyte_access.log`) and prints an access report: a header
with the event total and time span, then one tidy line per event.

## What's coming

Future versions will read CloudByte's staff roster to report activity per person and per
department.
