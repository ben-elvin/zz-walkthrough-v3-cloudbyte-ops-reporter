#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""


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
    user_counts = {}
    for record in records:
        username = record.split()[1]
        user_counts[username] = user_counts.get(username, 0) + 1

    user_pairs = []
    for username, count in user_counts.items():
        user_pairs.append((count, username))
    user_pairs.sort(reverse=True)
    print("Most active users")
    for rank, (count, username) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {username}: {count} events")


if __name__ == "__main__":
    main()
