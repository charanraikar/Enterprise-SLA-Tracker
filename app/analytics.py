from collections import Counter

from app.sla import calculate_resolution_minutes, get_sla_status


def _percent(part, whole):
    if whole == 0:
        return 0
    return round((part / whole) * 100, 2)


def build_summary(tickets):
    total = len(tickets)
    by_priority = Counter(ticket["priority"] for ticket in tickets)
    by_status = Counter(ticket["status"] for ticket in tickets)
    by_category = Counter(ticket["category"] for ticket in tickets)

    breached = 0
    resolution_minutes = []

    for ticket in tickets:
        sla_status = get_sla_status(
            ticket["priority"],
            ticket["created_at"],
            ticket["due_at"],
            ticket.get("resolved_at"),
        )
        if sla_status == "SLA Breached":
            breached += 1

        minutes = calculate_resolution_minutes(ticket["created_at"], ticket.get("resolved_at"))
        if minutes is not None:
            resolution_minutes.append(minutes)

    avg_resolution_minutes = 0
    if resolution_minutes:
        avg_resolution_minutes = round(sum(resolution_minutes) / len(resolution_minutes), 2)

    return {
        "total_tickets": total,
        "sla_breaches": breached,
        "sla_breach_percentage": _percent(breached, total),
        "average_resolution_minutes": avg_resolution_minutes,
        "by_priority": dict(by_priority),
        "by_status": dict(by_status),
        "top_issue_categories": dict(by_category.most_common(5)),
    }

