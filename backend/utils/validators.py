def require_fields(data, *fields):
    """Check that data (dict) contains the required fields. Returns (ok, missing_list)."""
    missing = [f for f in fields if f not in (data or {}) or data.get(f) is None]
    return (len(missing) == 0, missing)
