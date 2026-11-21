# Copperleaf Digital

**Copperleaf Digital** is a digital agency: we build web apps for our clients and keep them
running. Every project is a different client's app. Lucia, our product manager, speaks for the
client: when the client changes their mind, the change comes through her.

## The team
| Name | Role | Ask them about |
|---|---|---|
| Adam Clarke | Delivery manager | priorities, deadlines, what the client sees and when |
| Salma Idris | Senior engineer | the code, Flask, SQLite, how to approach a task |
| Kenji Watanabe | QA engineer | how something should behave, edge cases, failing checks |
| Lucia Fernandez | Product manager, the client's voice | what the client asked for and why |
| Mona Jaber | People partner | the internship, your workload, holidays |

## The client: Wheels
**Wheels** rents cars from a desk in Manama: thirty cars, from small city cars to vans and a
few luxury ones. Another agency built the site last year and then left. It works and customers
use it every day, but the renters keep reporting bugs and the client has a long list of
changes. That is our job now: fix, change and grow it, without breaking what works.

## What the site does today
- `/cars`: the fleet, cheapest first, and a page per car, `/cars/<id>`, with the insurance
  plans and a booking form.
- `/search`: the cars that are free between a pickup day and a return day.
- The app's JSON API: `GET /api/quote` (what a rental costs), `POST /api/bookings`,
  `GET /api/bookings/<code>`, `POST /api/bookings/<code>/cancel` and `/return`, and
  `POST /api/drivers`.
- `/bookings/<code>`: the invoice of a booking.
- Promo codes, a "pay in 3" provider (PayLater), a staff page and a CSV export under `/admin`.
- `/pick`: a page for an AI assistant that was never built.

## The client's rules
- **Rental days.** A rental is charged per 24 hours: picked up on the 20th and returned on the
  22nd is 2 days. A car picked up and returned on the same day is 1 day.
- **Busy cars.** A booking takes its car from the pickup day to the return day, both days
  included. Cancelled and returned bookings don't count.
- **Money off.** A promo code takes a percentage off the car's own price, never off the
  insurance or fees. A percentage is rounded half up to the fils.
- A booking's code is `WH-` and 1000 + its id: `WH-1001`, `WH-1002`, ...

The exact paths, texts and numbers of each change are on your task page in Darbni.

## House rules
- Money is stored in **fils** as whole numbers (1 BHD = 1000 fils) and shown as BHD with 3
  decimals: `12.000 BHD`. `money.bhd()` (the `bhd` template filter) does that for you.
- Times are Bahrain time (`Asia/Bahrain`). Always ask `clock.now()` or `clock.today()`, never
  `datetime.now()`.
- The weekend is Friday and Saturday.
- Dates are written `2026-11-20`. Our tests use that format.
- The database changes only through a new file in `wheels/migrations/` (see `wheels/db.py`).
- All code lives in the `wheels` package. Keep functions small and names clear.
- AI only through `wheels/ai.py` (see README), always with a fallback.
- Customers use this site every day: run `pytest` and try the page in your browser before you
  submit.
