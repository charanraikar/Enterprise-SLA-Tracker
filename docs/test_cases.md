# Test Cases

| Test Case | Input | Expected Result |
|---|---|---|
| High priority SLA calculation | Priority High, created at 10:00 | Due time is 14:00 |
| Medium priority SLA calculation | Priority Medium, created at 10:00 | Due time is next day 10:00 |
| SLA breach detection | High ticket resolved 30 minutes after due time | Status is SLA Breached |
| Resolution time calculation | Created at 10:00, resolved at 11:15 | Resolution time is 75 minutes |
| Create ticket API | Valid ticket payload | Ticket saved with due_at and Open status |
| Update status API | Status changed to Resolved | resolved_at is populated |
| Analytics summary API | Multiple tickets exist | Returns counts by priority, status and category |

## Postman Flow

1. Call `GET /health`.
2. Call `POST /tickets` with the sample ticket payload.
3. Call `GET /tickets` and copy the created ticket id.
4. Call `PATCH /tickets/{ticket_id}/status` with `{"status": "Resolved"}`.
5. Call `GET /analytics/summary`.
6. Call `GET /analytics/export.csv`.

