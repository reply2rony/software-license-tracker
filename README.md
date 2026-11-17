# Software License Tracker

A starter learning template for keeping track of the software
licences a small office pays for: what each licence is, who
supplies it, how many seats were bought, how many are actually
used, when it renews, and what it costs per year. It comes with
a starter script that summarises the tracker and flags the
renewals that need a decision. It is a learning template with
fictional sample data only. It is not a production tool, it
makes no claim about any real organisation, and it contains no
real company data and no invented metrics.

## What it is

- `docs/license-tracker-guide.md` — the guide: what a licence
  tracker is for, the four statuses, how to work the list, and
  the checks that catch real mistakes.
- `software-license-tracker.csv` — a small fictional sample
  tracker: 12 made-up licences across subscription and
  perpetual types, so you can run the script and see the shape
  of the output.
- `scripts/license-summary.py` — a starter Python script that
  reads a CSV in the sample shape and prints the counts by
  status, the seats bought against the seats used, the licences
  over their seat count, the licences renewing within 30 and
  60 days, and the total sample annual cost. Labelled a starter
  learning template; it is not a production tool.

## How to use

1. Read `docs/license-tracker-guide.md` first — it explains the
   statuses and how to work the list in order.
2. Run the script on the sample data:

```bash
python3 scripts/license-summary.py software-license-tracker.csv --as-of 2026-11-17
```

3. Copy the sample CSV, replace the sample rows with your own
   licences for your own systems, and re-run the script to see
   your own renewals. Never put real vendor account names,
   licence keys, or credentials in the file.
4. Decide the renewals first — renew, shrink, or cancel — and
   fix any licence that is over its seat count before the
   renewal date, not after it.

## What the sample output looks like

Running the script on the sample file, with the reference date
2026-11-17, gives, for the 12 fictional licences:

- By status: Active 7, Expiring soon 3, Expired 1, Unused 1
- Seats bought: 250, seats used: 214
- Total sample annual cost: $14,950
- Over seat count: Sample Antivirus Home — 26 used of 25 seats
- Renewing within 30 days: Sample Backup Tool — 2026-11-30
  (in 13 days, $750/year) and Sample Design Tool — 2026-12-05
  (in 18 days, $2,400/year)
- Renewing within 60 days adds Sample Endpoint Security —
  2026-12-20 (in 33 days, $3,000/year)
- Expired or past renewal date: Sample Project Tracker —
  renewal was 2026-10-30

Those numbers come from the fictional sample rows in the CSV,
not from any real organisation. Recount them yourself with the
script — that is the point of the exercise.

## Sample / Demo notice

All software names, vendors, seat counts, dates, and costs in
this repo are fictional samples for learning. The diagram in
`docs/diagram.png` is a locally generated illustration labelled
"Sample / Demo" — it is not a screenshot of a real system, and
this template does not claim any production use.

## License

MIT — see `LICENSE`.
