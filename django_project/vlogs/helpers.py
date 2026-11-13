def normalize_tags(value):
    """Return unique, lowercase comma-separated tags in their original order."""
    return ", ".join(dict.fromkeys(tag.strip().lower() for tag in value.split(",") if tag.strip()))
