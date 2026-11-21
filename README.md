# Wheels car rental

Wheels rents cars from a desk in Manama, and this is their live site: search, booking,
invoices, promo codes and a small JSON API for their app. Copperleaf Digital took it over from
another agency. You'll fix and change it task by task. Read `COMPANY.md` first: it has the
client's rules and the house rules.

## Your tasks
**Your exact task is in Darbni.** Open the task there and read its page: it has the rules and
the values (prices, codes, limits) for YOUR version. Every intern gets their own version, so a
solution copied from someone else will fail the tests.

## Run it
```
python -m venv .venv
.venv\Scripts\activate          # Windows (on macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
flask --app wheels run --debug
```
Open http://127.0.0.1:5000. The database is `wheels.sqlite`. Delete the file to start over
with the demo data: 30 cars, a demo driver (id 1) and the promo code `WELCOME10`.

Try the API with curl:
```
curl "http://127.0.0.1:5000/api/quote?car=4&start=2026-11-20&end=2026-11-22&insurance=basic"
curl -X POST http://127.0.0.1:5000/api/bookings -H "Content-Type: application/json" -d "{\"car\": 4, \"driver\": 1, \"start\": \"2026-11-20\", \"end\": \"2026-11-22\", \"insurance\": \"basic\"}"
```

## Test it
```
pytest
```
These tests are yours to run and extend. Darbni runs its own hidden tests on every submission,
each on a new, empty database: whatever your change needs (a table, a column, rows) must be
created by `create_app`, from `wheels/migrations/`.

## The database
`create_app` runs every NEW file in `wheels/migrations/`, in name order, once per database
(`wheels/db.py`). To add a table, a column, an index or rows, add a new file with a higher
number, like `0010_promo_dates.sql`. Never edit a file that already ran.

## The clock rule
Rental days, "today" and promo end dates depend on the date. Always get it from
`wheels/clock.py`:
```python
from wheels import clock

today = clock.today()   # Bahrain time
```
Never `datetime.now()` or `date.today()`: tests set the time with the app's `NOW` setting,
like `tests/conftest.py` does (`"NOW": "2026-11-17T10:00"`).

## The AI rule
All AI calls go through `wheels/ai.py`. Always call it like this:
```python
from wheels import ai

reply = ai.ask_llm(prompt)
```
Not `from wheels.ai import ask_llm`: Darbni's tests swap `ai.ask_llm` for a fake model, and
that import would keep the real one. `ask_llm` can fail, so always have a fallback.

On your machine there is no real model: `ask_llm` returns a demo reply. To see what your code
does when the AI is down, make it fail:
```
set WHEELS_AI=fail              # Windows cmd (PowerShell: $env:WHEELS_AI="fail")
export WHEELS_AI=fail           # macOS/Linux
flask --app wheels run --debug
```

## Where things are
| File | What it does |
|---|---|
| `wheels/__init__.py` | `create_app(config)`: builds the app and its database |
| `wheels/settings.py` | settings and secrets (from the environment on the server) |
| `wheels/pages.py` | home and about |
| `wheels/cars.py` | `/cars`, `/cars/<id>`, `find_car()` |
| `wheels/search.py` | `/search` |
| `wheels/availability.py` | `is_free()`: is a car free on those days? |
| `wheels/pricing.py` | rental days, the car's price, the insurance plans |
| `wheels/bookings.py` | the quote, booking, a booking's details, cancelling |
| `wheels/invoice.py` | the invoice page `/bookings/<code>` |
| `wheels/promo.py` | promo codes |
| `wheels/drivers.py` | drivers |
| `wheels/returns.py` | returning a car |
| `wheels/paylater.py` | the PayLater "pay in 3" pages |
| `wheels/assistant.py` | the "Pick a car" page |
| `wheels/admin.py` | staff pages under `/admin` |
| `wheels/faq.md` | the client's questions and answers |
| `wheels/clock.py` | `clock.now()`, `clock.today()`: the only way to read the time |
| `wheels/money.py` | `bhd(fils)`: `12000` shows as `12.000 BHD` |
| `wheels/db.py` | `db.connect()` and the migrations |
| `wheels/migrations/` | the database, one `.sql` file per change |
| `wheels/ai.py` | `ask_llm(prompt)`, the only way to call AI |
| `wheels/templates/` | `base.html` (header, footer), `_car_card.html` (a car in a list) and one template per page |
| `wheels/static/style.css` | the styles |
| `tests/` | pytest tests |
