import unittest
from datetime import datetime, timedelta

from app.sla import calculate_due_at, calculate_resolution_minutes, get_sla_status


class TestSlaLogic(unittest.TestCase):
    def test_high_priority_due_in_four_hours(self):
        created_at = datetime(2026, 9, 12, 10, 0, 0)
        due_at = calculate_due_at("High", created_at)
        self.assertEqual(due_at, created_at + timedelta(hours=4))

    def test_medium_priority_due_in_twenty_four_hours(self):
        created_at = datetime(2026, 9, 12, 10, 0, 0)
        due_at = calculate_due_at("Medium", created_at)
        self.assertEqual(due_at, created_at + timedelta(hours=24))

    def test_sla_breached_when_resolved_after_due_time(self):
        created_at = datetime(2026, 9, 12, 10, 0, 0)
        due_at = calculate_due_at("High", created_at)
        resolved_at = due_at + timedelta(minutes=30)
        self.assertEqual(get_sla_status("High", created_at, due_at, resolved_at), "SLA Breached")

    def test_resolution_minutes(self):
        created_at = datetime(2026, 9, 12, 10, 0, 0)
        resolved_at = datetime(2026, 9, 12, 11, 15, 0)
        self.assertEqual(calculate_resolution_minutes(created_at, resolved_at), 75)


if __name__ == "__main__":
    unittest.main()

