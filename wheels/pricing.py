"""Prices: how many days a rental is charged, the car's own price and the insurance plans."""

# The insurance plans a customer picks from. The key is what a booking stores.
INSURANCE = {
    "basic": {
        "name": "Basic cover",
        "daily_fils": 0,
        "about": "You pay the first 300 BHD of any damage.",
    },
    "full": {
        "name": "Full cover",
        "daily_fils": 2500,
        "about": "You pay nothing for damage.",
    },
}


def rental_days(start, end):
    """How many days a rental from `start` to `end` (two datetime.date) is charged."""
    return (end - start).days + 1


def car_total(daily_fils, days):
    """The price of the car itself for `days` days, in fils."""
    return daily_fils * days
