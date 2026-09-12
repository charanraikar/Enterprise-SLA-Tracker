# Enterprise Service Request Analytics and SLA Tracker

A FastAPI-based service request tracking prototype for managing client issues, monitoring SLA deadlines, and generating analytics for process improvement.

This project is inspired by real IT service management and consulting workflows, where teams must track client requests, assign ownership, meet agreed timelines, and report delivery performance.

## Overview

The system allows users to create service requests, assign priorities, track status changes, calculate SLA deadlines, detect SLA breaches, and view analytics such as ticket distribution, breach percentage, recurring issue categories, and resolution-time trends.

It demonstrates backend API development, relational database design, SLA business logic, API testing, documentation, and analytics reporting.

## Key Features

- Create and manage client service requests.
- Assign ticket priority, category, owner, and status.
- Automatically calculate SLA due time based on priority.
- Detect whether tickets are within SLA or breached.
- Update ticket status from `Open` to `In Progress`, `Resolved`, or `Closed`.
- Generate analytics summary for ticket counts, SLA breaches, priorities, statuses, and issue categories.
- Export ticket data as CSV for reporting or Power BI dashboarding.
- Includes Swagger UI, Postman collection, unit tests, SQL schema, and functional documentation.

## Tech Stack

| Area | Technology |
|---|---|
| Backend API | FastAPI |
| Local Database | SQLite |
| Relational DB Support | MySQL schema with PyMySQL configuration |
| Data Processing | Python |
| API Testing | Swagger UI, Postman |
| Testing | Python unittest |
| Documentation | Markdown |

## SLA Rules

| Priority | SLA Deadline |
|---|---:|
| High | 4 hours |
| Medium | 24 hours |
| Low | 48 hours |

If a ticket is resolved after its SLA deadline, it is marked as `SLA Breached`. Otherwise, it is marked as `Within SLA`.

## Project Structure

```text
enterprise_sla_tracker/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py              # FastAPI routes
â”‚   â”œâ”€â”€ database.py          # Database connection and ticket repository
â”‚   â”œâ”€â”€ sla.py               # SLA deadline and breach logic
â”‚   â”œâ”€â”€ analytics.py         # Analytics summary logic
â”‚   â”œâ”€â”€ schemas.py           # Request models
â”‚   â””â”€â”€ seed.py              # Sample ticket data
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ requirements.md
â”‚   â”œâ”€â”€ test_cases.md
â”‚   â”œâ”€â”€ release_notes.md
â”‚   â””â”€â”€ interview_explanation.md
â”œâ”€â”€ postman/
â”‚   â””â”€â”€ Service_Request_SLA_Tracker.postman_collection.json
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ export_sample_analytics.py
â”œâ”€â”€ sql/
â”‚   â””â”€â”€ mysql_schema.sql
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ test_sla_logic.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/charanraikar/Enterprise-SLA-Tracker.git
cd Enterprise-SLA-Tracker
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Seed sample tickets:

```bash
python -m app.seed
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/tickets` | Create a new service request |
| GET | `/tickets` | List all service requests |
| GET | `/tickets/{ticket_id}` | Get one ticket by ID |
| PATCH | `/tickets/{ticket_id}/status` | Update ticket status |
| GET | `/analytics/summary` | View SLA and ticket analytics |
| GET | `/analytics/export.csv` | Export ticket data as CSV |

## Example Request

Create a new ticket using `POST /tickets`:

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

Example response:

```json
{
  "id": 1,
  "client_name": "ABC Retail",
  "title": "Sales dashboard data mismatch",
  "category": "Data Issue",
  "priority": "High",
  "status": "Open",
  "owner": "Charan",
  "created_at": "2026-09-12 10:00:00",
  "due_at": "2026-09-12 14:00:00",
  "resolved_at": null,
  "sla_status": "Within SLA"
}
```

## Analytics Output

The `/analytics/summary` endpoint returns an overview like:

```json
{
  "total_tickets": 5,
  "sla_breaches": 2,
  "sla_breach_percentage": 40.0,
  "average_resolution_minutes": 380.0,
  "by_priority": {
    "High": 2,
    "Medium": 2,
    "Low": 1
  },
  "by_status": {
    "Open": 1,
    "In Progress": 1,
    "Resolved": 3
  },
  "top_issue_categories": {
    "Data Issue": 1,
    "Access Issue": 1,
    "Enhancement": 1,
    "Performance": 1,
    "UI Issue": 1
  }
}
```

## Run Tests

```bash
python -m unittest discover -s tests
```

The tests cover:

- SLA due-time calculation.
- SLA breach detection.
- Resolution-time calculation.

## Export Analytics CSV

```bash
python scripts/export_sample_analytics.py
```

This generates:

```text
data/ticket_export.csv
```

The CSV can be used for reporting or imported into Power BI.

## MySQL Setup

The project runs locally with SQLite by default. To use MySQL, create the database and table:

```bash
mysql -u root -p < sql/mysql_schema.sql
```

Set environment variables:

```bash
export DB_BACKEND=mysql
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=sla_tracker
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

For Windows PowerShell:

```powershell
$env:DB_BACKEND="mysql"
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DATABASE="sla_tracker"
python -m uvicorn app.main:app --reload
```

## What I Learned

- Designing REST APIs using FastAPI.
- Implementing business rules such as SLA deadline calculation.
- Building a relational ticket-tracking workflow.
- Writing unit tests for core logic.
- Preparing API documentation and Postman test flows.
- Generating analytics for process improvement decisions.

## Future Improvements

- Add user authentication and role-based access.
- Add email alerts for tickets nearing SLA breach.
- Add a frontend dashboard.
- Add Docker support.
- Publish Power BI dashboard screenshots.
- Add deployment on a cloud platform.

## Project Status

Completed as a self-built prototype for learning and demonstrating Technology Analyst / Consultant-style backend, testing, documentation, and analytics skills.
