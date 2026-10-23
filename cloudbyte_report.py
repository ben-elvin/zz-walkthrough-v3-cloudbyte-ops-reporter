#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""

import csv


def get_user(record):
    return record.split()[1]


def get_hour(record):
    return record.split()[0][11:13]


def get_action(record):
    return record.split()[2]


def by_count_then_name(pair):
    """Sort key: busiest first, ties broken A-to-Z by name."""
    count, name = pair
    return (-count, name)


def count_and_rank(records, get_key):
    """Return (count, key) pairs for the records, ranked most-frequent first."""
    counts = {}
    for record in records:
        key = get_key(record)
        counts[key] = counts.get(key, 0) + 1
    pairs = [(count, key) for key, count in counts.items()]
    pairs.sort(key=by_count_then_name)
    return pairs


def main():
    with open("cloudbyte_access.log") as f:
        records = [line for line in f]

    # Read the staff roster into a {username: department} lookup.
    with open("users.csv") as f:
        dept_of = {row["username"]: row["department"] for row in csv.DictReader(f)}

    first = records[0].split()[0]
    last = records[-1].split()[0]
    print("CloudByte Access Report")
    print(f"{len(records)} events from {first[:10]} {first[11:]} to {last[:10]} {last[11:]}")
    print()
    for record in records:
        fields = record.split()
        ts = fields[0]
        print(f"{ts[:10]} {ts[11:]}  {fields[1]} {fields[2]}")

    print()
    user_pairs = count_and_rank(records, get_user)
    print("Most active users")
    for rank, (count, username) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {username}: {count} events")

    print()
    hour_pairs = count_and_rank(records, get_hour)
    print("Busiest hours")
    for count, hour in hour_pairs:
        print(f"  {hour}:00  {count} events")

    print()
    action_pairs = count_and_rank(records, get_action)
    print("Activity by type")
    for rank, (count, action) in enumerate(action_pairs, start=1):
        print(f"  {rank}. {action}: {count} events")

    print()
    logins = [record for record in records if get_action(record) == "login"]
    login_pairs = count_and_rank(logins, get_user)
    print("Most active logins")
    for rank, (count, username) in enumerate(login_pairs, start=1):
        print(f"  {rank}. {username}: {count} events")

    print()
    person = "alice"
    person_records = [record for record in records if get_user(record) == person]
    person_pairs = count_and_rank(person_records, get_action)
    print(f"Activity for {person}")
    for rank, (count, action) in enumerate(person_pairs, start=1):
        print(f"  {rank}. {action}: {count} events")

    print()
    dept_counts = {}
    for count, username in user_pairs:
        dept = dept_of[username]
        dept_counts[dept] = dept_counts.get(dept, 0) + count
    dept_pairs = [(count, dept) for dept, count in dept_counts.items()]
    dept_pairs.sort(key=by_count_then_name)
    print("Activity by department")
    for rank, (count, dept) in enumerate(dept_pairs, start=1):
        print(f"  {rank}. {dept}: {count} events")


if __name__ == "__main__":
    main()
