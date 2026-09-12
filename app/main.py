from fastapi import FastAPI, HTTPException, Response

from app.analytics import build_summary
from app.database import TicketRepository
from app.schemas import TicketCreate, TicketStatusUpdate
from app.sla import get_sla_status


app = FastAPI(
    title="Enterprise Service Request Analytics and SLA Tracker",
    description="Prototype IT service request system with SLA tracking and analytics.",
    version="1.0.0",
)

repository = TicketRepository()


@app.on_event("startup")
def startup():
    repository.init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketCreate):
    try:
        saved = repository.create_ticket(ticket.dict())
        saved["sla_status"] = get_sla_status(saved["priority"], saved["created_at"], saved["due_at"])
        return saved
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/tickets")
def list_tickets(status: str | None = None):
    tickets = repository.list_tickets(status=status)
    for ticket in tickets:
        ticket["sla_status"] = get_sla_status(
            ticket["priority"],
            ticket["created_at"],
            ticket["due_at"],
            ticket.get("resolved_at"),
        )
    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    try:
        ticket = repository.get_ticket(ticket_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    ticket["sla_status"] = get_sla_status(
        ticket["priority"],
        ticket["created_at"],
        ticket["due_at"],
        ticket.get("resolved_at"),
    )
    return ticket


@app.patch("/tickets/{ticket_id}/status")
def update_status(ticket_id: int, payload: TicketStatusUpdate):
    try:
        ticket = repository.update_status(ticket_id, payload.status)
        ticket["sla_status"] = get_sla_status(
            ticket["priority"],
            ticket["created_at"],
            ticket["due_at"],
            ticket.get("resolved_at"),
        )
        return ticket
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/analytics/summary")
def analytics_summary():
    return build_summary(repository.list_tickets())


@app.get("/analytics/export.csv")
def analytics_export_csv():
    tickets = repository.list_tickets()
    header = "id,client_name,title,category,priority,status,owner,created_at,due_at,resolved_at,sla_status\n"
    rows = []
    for ticket in tickets:
        sla_status = get_sla_status(
            ticket["priority"],
            ticket["created_at"],
            ticket["due_at"],
            ticket.get("resolved_at"),
        )
        rows.append(
            ",".join(
                str(ticket.get(column, "") or "").replace(",", " ")
                for column in [
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
                ]
            )
            + f",{sla_status}"
        )
    return Response(content=header + "\n".join(rows), media_type="text/csv")

