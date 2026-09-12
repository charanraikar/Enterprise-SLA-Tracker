from datetime import UTC, datetime, timedelta


SLA_HOURS_BY_PRIORITY = {
    "High": 4,
    "Medium": 24,
    "Low": 48,
}

OPEN_STATUSES = {"Open", "In Progress"}
CLOSED_STATUSES = {"Resolved", "Closed"}
VALID_STATUSES = OPEN_STATUSES | CLOSED_STATUSES


def parse_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def calculate_due_at(priority, created_at=None):
    if priority not in SLA_HOURS_BY_PRIORITY:
        valid = ", ".join(SLA_HOURS_BY_PRIORITY)
        raise ValueError(f"Unknown priority '{priority}'. Expected one of: {valid}")

    created = parse_datetime(created_at) or datetime.now(UTC).replace(tzinfo=None)
    return created + timedelta(hours=SLA_HOURS_BY_PRIORITY[priority])


def calculate_resolution_minutes(created_at, resolved_at):
    created = parse_datetime(created_at)
    resolved = parse_datetime(resolved_at)
    if not created or not resolved:
        return None
    return round((resolved - created).total_seconds() / 60, 2)


def get_sla_status(priority, created_at, due_at=None, resolved_at=None, now=None):
    created = parse_datetime(created_at)
    due = parse_datetime(due_at) or calculate_due_at(priority, created)
    resolved = parse_datetime(resolved_at)
    check_time = resolved or parse_datetime(now) or datetime.now(UTC).replace(tzinfo=None)

    if check_time <= due:
        return "Within SLA"
    return "SLA Breached"


def is_valid_status(status):
    return status in VALID_STATUSES


def should_set_resolved_at(status):
    return status in CLOSED_STATUSES
