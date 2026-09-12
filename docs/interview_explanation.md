# Interview Explanation

## Simple Explanation

This project is a service request tracking system. In consulting and IT service companies, clients raise issues or requests. Each request must be solved within an agreed deadline called an SLA.

The system stores each request, assigns a priority, calculates the SLA deadline, tracks status changes and shows analytics such as SLA breaches and repeated issue categories.

## Why I Built It

I built it to understand how enterprise teams manage client support and delivery quality. The project combines application development, database design, API testing, documentation and data analysis.

## Architecture

1. FastAPI receives requests from users or Postman.
2. The ticket repository stores data in SQLite for local demo.
3. A MySQL schema is provided for a production-like relational database setup.
4. SLA logic calculates due time and breach status.
5. Analytics logic summarizes ticket data.
6. CSV export can be used for Power BI dashboards.

## Database Table

The main table is `tickets`.

Important columns:

- `client_name`
- `title`
- `category`
- `priority`
- `status`
- `owner`
- `created_at`
- `due_at`
- `resolved_at`

## How SLA Is Calculated

- High priority: created time plus 4 hours
- Medium priority: created time plus 24 hours
- Low priority: created time plus 48 hours

If the resolved time is later than the due time, it is marked as SLA Breached.

## What To Say If Asked Whether It Is Real

Say:

```text
It is a self-built prototype inspired by enterprise IT service management workflows. I built it to demonstrate application development, SLA logic, testing, documentation and analytics.
```

## Questions They May Ask

| Question | Short Answer |
|---|---|
| Why FastAPI? | It is lightweight, fast and good for building REST APIs quickly. |
| Why SLA tracking? | Consulting teams need to meet client timelines and monitor delivery quality. |
| How do you detect a breach? | Compare resolved time or current time with the due_at timestamp. |
| What database did you use? | SQLite for local demo and a MySQL-ready schema for relational deployment. |
| What did you test? | SLA deadline calculation, breach detection and resolution-time calculation. |
| How can this be improved? | Add authentication, role-based access, email alerts and Power BI dashboard publishing. |

