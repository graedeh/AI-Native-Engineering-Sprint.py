import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    get_ticket,
    next_ticket_id,
)


class TicketTests(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_high_urgency_and_12_users_is_critical(self):
        self.assertEqual(
            calculate_priority("high", 12),
            "critical"
        )

    def test_high_urgency_and_2_users_is_high(self):
        self.assertEqual(
            calculate_priority("high", 2),
            "high"
        )

    def test_low_urgency_and_4_users_is_medium(self):
        self.assertEqual(
            calculate_priority("low", 4),
            "medium"
        )

    def test_low_urgency_and_1_user_is_low(self):
        self.assertEqual(
            calculate_priority("low", 1),
            "low"
        )

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "Wi-Fi down",
                "Network",
                "high",
                0,
            )

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "  ",
                "Network",
                "high",
                2,
            )

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "Issue",
                "Food",
                "low",
                1,
            )

    def test_category_and_urgency_are_normalized(self):
        ticket = create_ticket(
            self.tickets,
            " Wi-Fi ",
            "network",
            "HIGH",
            12,
        )

        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["title"], "Wi-Fi")

    def test_ticket_ids_are_unique_and_increment(self):
        first = create_ticket(
            self.tickets, "Issue one", "Other", "low", 1
        )

        second = create_ticket(
            self.tickets, "Issue two", "Other", "low", 1
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_next_id_uses_existing_ids_after_reload(self):
        self.assertEqual(
            next_ticket_id([{"id": "T004"}]),
            "T005"
        )

    def test_get_ticket_returns_none_for_unknown_id(self):
        self.assertIsNone(
            get_ticket(self.tickets, "T999")
        )


if __name__ == "__main__":
    unittest.main()