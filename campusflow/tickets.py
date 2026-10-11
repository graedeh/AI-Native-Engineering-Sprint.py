"""Ticket creation, validation, lookup, and priority calculation."""

CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

URGENCY_LEVELS = {"low", "medium", "high"}

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def calculate_priority(urgency, affected_users):
    """Calculate ticket priority using the project rules."""
    urgency = urgency.strip().lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def validate_ticket_details(title, category, urgency, affected_users):
    """Validate and normalize ticket details."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title must not be blank.")

    if (
        not isinstance(category, str)
        or category.strip().lower() not in CATEGORIES
    ):
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    if (
        not isinstance(urgency, str)
        or urgency.strip().lower() not in URGENCY_LEVELS
    ):
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(
        affected_users, int
    ):
        raise ValueError("Affected users must be a positive whole number.")

    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return (
        title.strip(),
        CATEGORIES[category.strip().lower()],
        urgency.strip().lower(),
        affected_users,
    )


def next_ticket_id(tickets):
    """Generate the next ticket ID, including after reloading saved tickets."""

    highest = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            number = ticket_id[1:]

            if number.isdigit():
                highest = max(highest, int(number))

    return f"T{highest + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate details, create a ticket, store it, and return it."""

    title, category, urgency, affected_users = validate_ticket_details(
        title, category, urgency, affected_users
    )

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)

    return ticket


def get_ticket(tickets, ticket_id):
    """Find and return a ticket, or return None if it does not exist."""

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket

    return None