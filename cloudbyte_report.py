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


if __name__ == "__main__":
    main()
