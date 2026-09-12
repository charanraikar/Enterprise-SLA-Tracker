# Functional Requirements

## Objective

Build a prototype system for tracking client service requests and monitoring SLA performance.

## Users

- Service analyst
- Developer or ticket owner
- Team lead or reporting stakeholder

## Features

1. Create a new client service request with client name, issue title, category, priority and owner.
2. Automatically calculate SLA due time based on priority.
3. View all tickets and filter tickets by status.
4. Update ticket status to Open, In Progress, Resolved or Closed.
5. Mark resolution time when a ticket is resolved or closed.
6. Identify whether a ticket is within SLA or breached.
7. Generate summary analytics for SLA breaches, status counts, priority counts and top categories.
8. Export ticket data as CSV for dashboarding or Power BI.

## Non-Functional Requirements

- APIs should return JSON responses.
- Ticket data should persist in a relational database.
- SLA rules should be separated from API route logic.
- Test cases should cover SLA deadline and breach calculation.
- Documentation should explain setup, APIs and testing steps.

