from datetime import UTC, datetime, timedelta

from app.database import TicketRepository


def main():
    repo = TicketRepository()
    repo.init_db()

    base_time = datetime.now(UTC).replace(tzinfo=None, microsecond=0) - timedelta(days=2)
    sample_tickets = [
        {
            "client_name": "ABC Retail",
            "title": "Sales dashboard data mismatch",
            "description": "Dashboard totals do not match the monthly source report.",
            "category": "Data Issue",
            "priority": "High",
            "owner": "Charan",
            "created_at": base_time,
            "status": "Resolved",
            "resolved_at": base_time + timedelta(hours=3),
        },
        {
            "client_name": "FinServe India",
            "title": "Login failure for operations team",
            "description": "Multiple users are unable to log in after password reset.",
            "category": "Access Issue",
            "priority": "High",
            "owner": "Charan",
            "created_at": base_time + timedelta(hours=2),
            "status": "Resolved",
            "resolved_at": base_time + timedelta(hours=8),
        },
        {
            "client_name": "Northstar Logistics",
            "title": "Add filter to shipment report",
            "description": "Client requested a new region filter in the shipment report.",
            "category": "Enhancement",
            "priority": "Medium",
            "owner": "Charan",
            "created_at": base_time + timedelta(hours=6),
            "status": "In Progress",
        },
        {
            "client_name": "Medix Care",
            "title": "Slow response from analytics API",
            "description": "Analytics API response time is high during peak usage.",
            "category": "Performance",
            "priority": "Medium",
            "owner": "Charan",
            "created_at": base_time + timedelta(hours=10),
            "status": "Resolved",
            "resolved_at": base_time + timedelta(hours=20),
        },
        {
            "client_name": "EduPrime",
            "title": "Typo in monthly report label",
            "description": "Report label has spelling issue in exported PDF.",
            "category": "UI Issue",
            "priority": "Low",
            "owner": "Charan",
            "created_at": base_time + timedelta(hours=16),
        },
    ]

    for ticket in sample_tickets:
        repo.create_ticket(ticket)

    print("Seeded sample tickets.")


if __name__ == "__main__":
    main()
