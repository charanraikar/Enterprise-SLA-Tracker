import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.analytics import build_summary
from app.database import TicketRepository
from app.sla import get_sla_status


def main():
    repo = TicketRepository()
    repo.init_db()
    tickets = repo.list_tickets()
    os.makedirs("data", exist_ok=True)

    with open("data/ticket_export.csv", "w", newline="", encoding="utf-8") as output:
        fieldnames = [
            "id",
            "client_name",
            "title",
            "category",
            "priority",
            "status",
            "owner",
            "created_at",
            "due_at",
            "resolved_at",
            "sla_status",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for ticket in tickets:
            row = {field: ticket.get(field, "") for field in fieldnames}
            row["sla_status"] = get_sla_status(
                ticket["priority"],
                ticket["created_at"],
                ticket["due_at"],
                ticket.get("resolved_at"),
            )
            writer.writerow(row)

    summary = build_summary(tickets)
    print(summary)
    print("Exported data/ticket_export.csv")


if __name__ == "__main__":
    main()

