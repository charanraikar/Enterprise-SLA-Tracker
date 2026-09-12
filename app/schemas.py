from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    client_name: str = Field(..., example="ABC Retail")
    title: str = Field(..., example="Sales dashboard data mismatch")
    description: str = Field(..., example="Client reported mismatch between dashboard and source report")
    category: str = Field(..., example="Data Issue")
    priority: str = Field(..., example="High")
    owner: str = Field(..., example="Charan")


class TicketStatusUpdate(BaseModel):
    status: str = Field(..., example="Resolved")

