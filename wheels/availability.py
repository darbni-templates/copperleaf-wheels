"""When is a car free? A booking takes its car from the pickup day to the return day, both days
included. Only bookings with status "booked" count: a returned or cancelled car is free again."""


def is_free(conn, car_id, start, end, ignore=None):
    """True if no booking of this car overlaps start..end (two datetime.date). `ignore`: the id of
    a booking to leave out, for a booking that moves to new dates."""
    row = conn.execute(
        "SELECT 1 FROM bookings WHERE car_id = ? AND status = 'booked'"
        " AND start_date <= ? AND end_date >= ? AND id IS NOT ? LIMIT 1",
        (car_id, end.isoformat(), start.isoformat(), ignore),
    ).fetchone()
    return row is None
