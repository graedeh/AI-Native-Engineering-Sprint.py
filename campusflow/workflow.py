"""Ticket assignment, status changes, and work-queue ordering."""

from campusflow.tickets import PRIORITY_ORDER, get_ticket


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an unresolved ticket to a staff member."""

    ticket = get_ticket(tickets, ticket_id)

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} was not found.")

    if ticket["status"] == "resolved":
        raise ValueError("Reopen a resolved ticket before modifying it.")

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name must not be blank.")

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def change_status(tickets, ticket_id, new_status):
    """Change ticket status according to the allowed workflow."""

    ticket = get_ticket(tickets, ticket_id)

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} was not found.")

    if new_status not in {"open", "in_progress", "resolved"}:
        raise ValueError(
            "Status must be open, in_progress, or resolved."
        )

    current = ticket["status"]

    if current == "resolved":
        if new_status == "open":
            ticket["status"] = "open"
            return ticket

        raise ValueError(
            "A resolved ticket must be reopened to open first."
        )

    if current == "open" and new_status == "in_progress":
        if not ticket["assigned_to"]:
            raise ValueError(
                "Assign the ticket before moving it to in_progress."
            )

        ticket["status"] = "in_progress"
        return ticket

    if current == "in_progress" and new_status == "resolved":
        ticket["status"] = "resolved"
        return ticket

    if current == new_status:
        raise ValueError(f"Ticket is already in status {new_status}.")

    raise ValueError(
        f"Invalid status transition: {current} -> {new_status}."
    )


def _ticket_number(ticket):
    """Extract the numeric part of a ticket ID."""

    ticket_id = ticket.get("id", "T0")

    digits = ticket_id[1:] if isinstance(ticket_id, str) else ""

    return int(digits) if digits.isdigit() else 0


def get_work_queue(tickets):
    """Return unresolved tickets ordered by priority and ticket ID."""

    unresolved = [
        ticket
        for ticket in tickets
        if ticket.get("status") in {"open", "in_progress"}
    ]

    return sorted(
        unresolved,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket.get("priority"), 99),
            _ticket_number(ticket),
        ),
    )