#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""


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
    pairs = []
    for key, count in counts.items():
        pairs.append((count, key))
    pairs.sort(key=by_count_then_name)
    return pairs


def main():
    records = []
    with open("cloudbyte_access.log") as f:
        for line in f:
            records.append(line)

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


if __name__ == "__main__":
    main()
