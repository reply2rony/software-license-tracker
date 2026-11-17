#!/usr/bin/env python3
"""Starter learning template: summarise a software license tracker CSV.

Usage:
    python3 scripts/license-summary.py software-license-tracker.csv
    python3 scripts/license-summary.py software-license-tracker.csv --as-of 2026-11-17

Reads a CSV with columns: software, vendor, license_type, seats,
seats_used, renewal_date, annual_cost_usd, status, owner, note.
Status must be one of: Active, Expiring soon, Expired, Unused.
Prints the total licenses, the counts by status, the total seats
bought and used, the licenses over their seat count, the licenses
renewing within 30 and 60 days of the reference date, and the
total sample annual cost. Sample data only; it is not a
production tool. Always check the tracker against the real
licenses and vendor records before trusting it.
"""
import argparse
import csv
import datetime
import sys
from collections import defaultdict

VALID_STATUSES = ("Active", "Expiring soon", "Expired", "Unused")


def parse_date(text, line_no):
    try:
        return datetime.date.fromisoformat(text.strip())
    except ValueError:
        print(f"Line {line_no}: renewal_date '{text}' is not a YYYY-MM-DD date.")
        raise SystemExit(1)


def parse_int(text, column, line_no):
    try:
        value = int(text)
    except ValueError:
        print(f"Line {line_no}: {column} '{text}' is not a whole number.")
        raise SystemExit(1)
    if value < 0:
        print(f"Line {line_no}: {column} '{text}' cannot be negative.")
        raise SystemExit(1)
    return value


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"software", "vendor", "license_type", "seats",
                    "seats_used", "renewal_date", "annual_cost_usd", "status"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            print(f"CSV must have columns: {', '.join(sorted(required))}")
            raise SystemExit(1)
        for line_no, row in enumerate(reader, start=2):
            status = row["status"].strip()
            if status not in VALID_STATUSES:
                print(f"Line {line_no}: status '{status}' is not one of "
                      f"{', '.join(VALID_STATUSES)}.")
                raise SystemExit(1)
            rows.append({
                "software": row["software"].strip(),
                "vendor": row["vendor"].strip(),
                "license_type": row["license_type"].strip(),
                "seats": parse_int(row["seats"], "seats", line_no),
                "seats_used": parse_int(row["seats_used"], "seats_used", line_no),
                "renewal_date": parse_date(row["renewal_date"], line_no),
                "annual_cost_usd": parse_int(row["annual_cost_usd"],
                                             "annual_cost_usd", line_no),
                "status": status,
            })
    return rows


def print_table(title, groups):
    print(title)
    for name in sorted(groups, key=lambda k: groups[k], reverse=True):
        print(f"  {name:<15} {groups[name]}")
    print()


def main():
    ap = argparse.ArgumentParser(
        description="Summarise a software license tracker CSV.")
    ap.add_argument("csv_file", help="path to the CSV file to summarise")
    ap.add_argument("--as-of", default=None,
                    help="reference date YYYY-MM-DD (default: today)")
    args = ap.parse_args()

    if args.as_of:
        try:
            ref = datetime.date.fromisoformat(args.as_of)
        except ValueError:
            print(f"--as-of '{args.as_of}' is not a YYYY-MM-DD date.")
            raise SystemExit(1)
    else:
        ref = datetime.date.today()

    try:
        rows = load_rows(args.csv_file)
    except FileNotFoundError:
        print(f"File not found: {args.csv_file}")
        raise SystemExit(1)

    if not rows:
        print("No data rows found in the CSV.")
        raise SystemExit(1)

    total = len(rows)
    by_status = defaultdict(int)
    for row in rows:
        by_status[row["status"]] += 1

    seats = sum(r["seats"] for r in rows)
    used = sum(r["seats_used"] for r in rows)
    total_cost = sum(r["annual_cost_usd"] for r in rows)

    print(f"Reference date: {ref.isoformat()}")
    print(f"Licenses: {total}")
    print(f"Seats bought: {seats}, seats used: {used}")
    print(f"Total sample annual cost: ${total_cost:,}")
    print()
    print_table("By status:", by_status)

    over = [r for r in rows if r["seats_used"] > r["seats"]]
    print("Over seat count (more users than seats bought):")
    if over:
        for row in over:
            print(f"  {row['software']} - {row['seats_used']} used of "
                  f"{row['seats']} seats")
    else:
        print("  None.")
    print()

    for window in (30, 60):
        upcoming = [r for r in rows
                    if r["status"] != "Expired"
                    and 0 <= (r["renewal_date"] - ref).days <= window]
        print(f"Renewing within {window} days:")
        if upcoming:
            for row in sorted(upcoming, key=lambda r: r["renewal_date"]):
                days = (row["renewal_date"] - ref).days
                print(f"  {row['software']} - {row['renewal_date'].isoformat()} "
                      f"(in {days} days, ${row['annual_cost_usd']:,}/year)")
        else:
            print("  None.")
        print()

    overdue = [r for r in rows
               if r["status"] == "Expired" or r["renewal_date"] < ref]
    print("Expired or past renewal date:")
    if overdue:
        for row in overdue:
            print(f"  {row['software']} - renewal was "
                  f"{row['renewal_date'].isoformat()} [{row['status']}]")
    else:
        print("  None.")
    print()
    print("Check before using: compare the tracker with the vendor's")
    print("own records. A row in a spreadsheet is not proof a license")
    print("is paid, current, or still in use.")


if __name__ == "__main__":
    main()
