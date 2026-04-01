"""Shared calculation helpers used across services."""


def calculate_percent_change(old_value: float, new_value: float) -> float:
    """Return percent change while safely handling zero denominators."""
    if old_value == 0:
        return 0.0
    return round(((new_value - old_value) / old_value) * 100, 2)
