-- Wheels' tables, as launched. Money in fils, dates as 2026-11-20.
CREATE TABLE cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,         -- economy, compact, suv, van, luxury, sports
    transmission TEXT NOT NULL,     -- automatic or manual
    seats INTEGER NOT NULL,
    daily_fils INTEGER NOT NULL
);

CREATE TABLE drivers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    licence TEXT NOT NULL
);

CREATE TABLE promos (
    code TEXT PRIMARY KEY,          -- in capitals
    percent INTEGER NOT NULL        -- off the car's own price
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars (id),
    driver_id INTEGER NOT NULL REFERENCES drivers (id),
    start_date TEXT NOT NULL,       -- the pickup day
    end_date TEXT NOT NULL,         -- the return day
    insurance TEXT NOT NULL,        -- a key of pricing.INSURANCE
    promo_code TEXT,
    total_fils INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'booked',  -- booked, returned or cancelled
    created_at TEXT NOT NULL
);
