"""Promo codes: a code gives a percentage off the car's own price (not off the insurance)."""


class PromoError(Exception):
    """A code that can't be used. str(error) is the message for the customer."""


def find(conn, code):
    """The promo row (code, percent) of this code, or None. Codes are stored in capitals."""
    return conn.execute("SELECT * FROM promos WHERE code = ?", (code.strip().upper(),)).fetchone()


def check(conn, code):
    """The promo row of a code a customer typed in. Raises PromoError if it can't be used."""
    row = find(conn, code)
    if row is None:
        raise PromoError("unknown promo code")
    return row
