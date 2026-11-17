# Software License Tracker — Starter Guide

A starter guide to keeping track of the software licences a
small office pays for: what each licence is, who supplies it,
how many seats were bought, how many are actually used, when
it renews, and what it costs per year. This guide explains the
shape of the work and the checks to run. All examples are
fictional samples for learning. This template does not describe
any real organisation, real systems, or production use.

## What a licence tracker is for

Software licences are easy to lose track of: a subscription
auto-renews after nobody used it for a year, a team grows past
the seats it bought, or a renewal date slips past and a tool
stops working on a Monday morning. A tracker keeps one row per
licence so those three surprises — paying for nothing, using
more than was bought, and missing a renewal — are visible
before they cost money. The script in this repo,
`scripts/license-summary.py`, is a starter example of how to
read that tracker: it prints the counts by status, the seats
bought against the seats used, the licences over their seat
count, the licences renewing within 30 and 60 days, and the
total sample annual cost.

## The tracker shape

The script expects a CSV with these columns:

| Column | Meaning | Example (fictional) |
|--------|---------|---------------------|
| software | The product name | Sample Design Tool |
| vendor | Who supplies it | Sample Vendor B |
| license_type | Subscription or Perpetual | Subscription |
| seats | Seats bought | 10 |
| seats_used | Seats actually in use | 9 |
| renewal_date | Next renewal, YYYY-MM-DD | 2026-12-05 |
| annual_cost_usd | Cost per year in USD | 2400 |
| status | Active, Expiring soon, Expired, or Unused | Expiring soon |
| owner | Who is responsible (sample names only) | Sample owner - IT lead |
| note | A short human note (optional) | Sample item - renew or lose the design seats |

Keep the shape fixed: same column names, same order, one row
per licence, and only the four exact status values — the script
rejects anything else so a typo cannot silently become an
"Active" licence.

## The four statuses

1. **Active** — paid, current, and in use. The ordinary state.
   Check the seats used against the seats bought: a licence
   with far fewer users than seats is a candidate to shrink at
   renewal.
2. **Expiring soon** — renews in the near future and needs a
   decision now: renew, shrink, or cancel. Mark a licence this
   way as soon as its renewal comes inside your decision
   window, not on the day it renews.
3. **Expired** — the renewal date has passed. Either renew it
   or stop using the software. An expired licence that is still
   in use is the row that needs attention first.
4. **Unused** — bought but nobody uses it. The cheapest saving
   in any tracker is cancelling a licence with zero seats used.

## Working the list

1. **Copy the sample CSV** and replace the sample rows with
   your own licences for your own systems. Never put real
   vendor account names, licence keys, or credentials in the
   file.
2. **Run the script** to see where the list stands:
   `python3 scripts/license-summary.py software-license-tracker.csv`
   Add `--as-of YYYY-MM-DD` to check the renewals from a
   different reference date.
3. **Decide the renewals first.** The script lists the licences
   renewing within 30 days — that is your next work, in order.
   For each one, decide renew, shrink, or cancel before the
   date, not after it.
4. **Fix the seat counts.** If more people use a licence than
   seats were bought, buy a seat or remove a user — running
   over the count is a compliance problem, not a bargain. If
   far fewer seats are used than bought, shrink at renewal.
5. **Review monthly.** Licences change fast: people join and
   leave, tools are swapped, prices move. Re-run the script
   each month and add or retire rows as the licences change.

## Checks that catch real mistakes

- **Status spelling.** Only `Active`, `Expiring soon`, `Expired`,
  and `Unused` are accepted. The script stops on anything else,
  so a typo like "active" or "Expiring" is caught instead of
  silently counted as nothing.
- **Dates must be real dates.** The renewal date must be a valid
  `YYYY-MM-DD` date. The script stops on anything else, so a
  mistyped month cannot hide a renewal.
- **Seats used must not exceed seats bought.** The script lists
  every licence over its seat count separately — that list is a
  finding, not a footnote.
- **Two cuts must agree.** The counts by status must add up to
  the same total as the number of rows. In the sample data:
  Active 7 + Expiring soon 3 + Expired 1 + Unused 1 = 12, and
  there are 12 rows. If the two disagree, a row is miscategorised
  or missing.
- **Verify, do not assume.** Check the tracker against the
  vendor's own records: the renewal date on the invoice, the
  seat count in the vendor portal, the users who actually sign
  in. A tick in a spreadsheet is not a test.

## What this template does not do

- It does not pay, renew, or cancel any licence — it only tracks
  them. Every renewal is done by hand, in your own vendor
  accounts, by someone with the right access.
- It does not store licence keys, vendor passwords, or account
  details. Those belong in your organisation's own secure store,
  never in a repo.
- It does not check whether the software is actually installed
  or used. Seat counts come from the vendor portal and from
  asking the team, not from this file.

## Sample / Demo notice

All software names, vendors, seat counts, dates, and costs in
this repo are fictional samples for learning. The diagram in
`docs/diagram.png` is a locally generated illustration labelled
"Sample / Demo" — it is not a screenshot of a real system, and
this template does not claim any production use.
