# Deploy notes

## The host

The reporter runs on an EC2 instance (Amazon Linux 2023) that the instructor
set up for this course. Its address is in the instructor's message for the
deploy section; it is left out of this file because this repository is public.
Below, `<HOST-IP>` stands for that address.

## Getting on

The key is saved at `~/.ssh/cloudbyte-ops.pem` (mode 600) on my laptop, never
in this repository. Connect with:

    ssh -i ~/.ssh/cloudbyte-ops.pem ec2-user@<HOST-IP>

The account is `ec2-user`. The first connection asks to confirm the host's
fingerprint: answer `yes`. On the host the prompt reads
`[ec2-user@ip-172-31-41-213 ~]$`. `exit` comes back off.

## The host's clock

The host's clock is UTC and mine is not. On 23 October 2026 the host read
14:29 UTC while my laptop read 16:24 CEST (UTC+2). Any hour set on the host
is that hour in UTC, not that hour in my morning. From 25 October my laptop
is on CET (UTC+1), so the gap drops to one hour.

## Interpreter

The host runs Python 3.9.25 (`python3`, at `/usr/bin/python3`); my laptop's
project venv runs 3.13.5. The difference is expected. My virtual environment
is a folder on my laptop and does not travel; nothing needs installing on the
host, because the reporter imports only the standard library.

## What travelled, and where it lives

Three files, all in one folder on the host, `/home/ec2-user/ops`:

- `/home/ec2-user/ops/cloudbyte_report.py`, the reporter, copied unedited.
- `/home/ec2-user/ops/cloudbyte_access.log`, the access log it reads by default.
- `/home/ec2-user/ops/users.csv`, the roster it joins against by default.

Nothing else travels: not `.venv/`, not the README. The reporter finds the two
data files by bare name, which only works when the run starts in that folder,
so anything that starts it from elsewhere must pass their full paths.

Copied up from the project folder on my laptop with:

    scp -i ~/.ssh/cloudbyte-ops.pem cloudbyte_report.py cloudbyte_access.log users.csv ec2-user@<HOST-IP>:/home/ec2-user/ops/

A hand run on the host (`cd ~/ops && python3 cloudbyte_report.py -v > host-report.txt`)
gave a report identical to my laptop's (`diff` printed nothing).

## What starts it, and when

`cron` (package `cronie`, daemon `crond`) runs it from **ec2-user's own
crontab**, not root's. Check the daemon with `systemctl is-active crond`
(answer: `active`) and the entry with `crontab -l` (run as ec2-user, no
`sudo`). The entry is:

    0 5 * * * /usr/bin/python3 /home/ec2-user/ops/cloudbyte_report.py -v --roster /home/ec2-user/ops/users.csv /home/ec2-user/ops/cloudbyte_access.log > /home/ec2-user/report.txt 2> /home/ec2-user/cron-report.err

`0 5 * * *` is **05:00 UTC every day, on the host's clock**. Kate wants the
report by 07:00 in our office: 05:00 UTC is 07:00 in summer time (CEST) and
06:00 in winter time (CET), so it is ready in time all year.

Everything is written out in full because a cron run starts in
`/home/ec2-user`, not in `ops`, and gets a `PATH` of only `/usr/bin:/bin`.
`-v` is in the entry on purpose: without it the notices file stays empty
even on a good run.

## Where the two channels go

- The report (standard output, `>`) goes to `/home/ec2-user/report.txt`.
  This is the file Kate reads.
- The notices (standard error, `2>`) go to `/home/ec2-user/cron-report.err`.
- Both files are rewritten on every firing, so they always describe the most
  recent one.

## Checking on the last firing

Get onto the host (see "Getting on") and take these four readings, in order:

1. `crontab -l` — the entry above must be there. If it is missing, nothing has
   been firing and the files below are old.
2. `ls -l ~/report.txt ~/cron-report.err` — both times should be today, just
   after 05:00 UTC. An older time means the job has not run since then.
3. `head -1 ~/report.txt` and `wc -l < ~/report.txt` — a good report opens on
   `CloudByte Access Report` and has **118** lines. 0 lines (a zero-byte file)
   means the run stopped before printing anything; read step 4. A first line
   starting `INFO:` means the two channels were sent to the same file.
4. `cat ~/cron-report.err` — a good run leaves exactly two lines:

       INFO: loaded 45 records from /home/ec2-user/ops/cloudbyte_access.log
       INFO: no --user given; skipping the per-user report

   A `WARNING: skipping line N` means a malformed log line was skipped; the
   report still ran. A traceback means the run stopped: its last line names
   the file it could not find (for example
   `FileNotFoundError: ... '/home/ec2-user/ops/users.csv'` when the roster has
   been moved or renamed).

Tested on 23 October 2026 by renaming `users.csv`: readings 3 and 4 caught it
(0-line report, that `FileNotFoundError`), and both went back to normal on the
next firing after the file was restored.

## Optional extras on the host

Two more entries sit in the same crontab:

    1 5 * * * sleep 15; echo "..." >> /home/ec2-user/firings.log
    2 5 * * * sleep 30; /usr/bin/python3 /home/ec2-user/ops/report_health.py /home/ec2-user/report.txt 2> /home/ec2-user/watchdog.err

- `/home/ec2-user/firings.log` gains one line per day: the UTC time, the
  report's line count (118 is good) and its first line. It is never
  rewritten, so it answers "has this been running all month?".
- `/home/ec2-user/ops/report_health.py` is a watchdog: silent on a good report,
  one `UNHEALTHY: ...` line in `/home/ec2-user/watchdog.err` on a bad one.
  An empty `watchdog.err` after a firing means the report looked healthy.
  The watchdog is not part of this repository.
- In a crontab a bare `%` means a newline, so the `date` format in the log
  entry is written `\%Y-\%m-\%d...`.
