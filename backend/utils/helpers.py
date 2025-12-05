def to_dict(model):
    """Convert a SQLAlchemy model instance to a simple dict.
    This is a beginner-friendly serializer that loops over columns.
    """
    try:
        data = {}
        for col in model.__table__.columns:
            val = getattr(model, col.name)
            # if value is bytes or non-serializable, convert to string
            try:
                data[col.name] = val
            except Exception:
                data[col.name] = str(val)
        return data
    except Exception:
        return {}
