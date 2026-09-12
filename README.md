# Enterprise Service Request Analytics and SLA Tracker

A small FastAPI prototype for managing client service requests, tracking SLA deadlines and producing analytics for process improvement.

This project is designed to match Technology Analyst / Consultant-style work:

- Understand business requirements and convert them into API features.
- Build application APIs for ticket creation, status tracking and ownership.
- Track SLA deadlines based on priority.
- Analyse service data to find SLA breaches, repeated issue categories and resolution trends.
- Prepare API tests, functional documentation and release notes.

## What Problem It Solves

In IT service and consulting teams, clients raise issues or requests. Each request has a priority and a deadline called an SLA. If a high-priority issue is not resolved within its SLA time, it becomes a breach.

This project helps a team:

- Create and store service requests.
- Assign each request to an owner.
- Track status changes from Open to In Progress to Resolved or Closed.
- Calculate whether each request is within SLA or breached.
- Export ticket data for dashboarding or Power BI.

## Tech Stack

- Backend: FastAPI
- Local database: SQLite
- MySQL support: MySQL schema and optional PyMySQL configuration
- Data analysis: Python analytics module and CSV export
- Testing: Python unittest
- API testing: Postman collection

## SLA Rules

| Priority | SLA Deadline |
|---|---:|
| High | 4 hours |
| Medium | 24 hours |
| Low | 48 hours |

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Seed sample tickets:

```bash
python -m app.seed
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Main APIs

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check service health |
| POST | `/tickets` | Create a new service request |
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{ticket_id}` | View one ticket |
| PATCH | `/tickets/{ticket_id}/status` | Update ticket status |
| GET | `/analytics/summary` | View SLA and ticket analytics |
| GET | `/analytics/export.csv` | Export data for dashboarding |

## Example Ticket

```json
{
  "client_name": "ABC Retail",
  "title": "Sales dashboard data mismatch",
  "description": "Client reported mismatch between dashboard and source report",
  "category": "Data Issue",
  "priority": "High",
  "owner": "Charan"
}
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## MySQL Setup

For a MySQL version, create the database using:

```bash
mysql -u root -p < sql/mysql_schema.sql
```

Then run with:

```bash
export DB_BACKEND=mysql
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=sla_tracker
uvicorn app.main:app --reload
```



Be honest if asked:

```text
This was a self-built prototype inspired by enterprise service management workflows, not a company project.
```

