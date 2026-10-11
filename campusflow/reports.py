"""Ticket summary reporting."""

from collections import Counter

STATUSES = ("open", "in_progress", "resolved")

PRIORITIES = ("critical", "high", "medium", "low")


def build_report(tickets):
    """Build ticket totals and status/priority breakdowns."""

    status_counts = Counter(
        ticket.get("status") for ticket in tickets
    )

    priority_counts = Counter(
        ticket.get("priority") for ticket in tickets
    )

    return {
        "total": len(tickets),

        "by_status": {
            status: status_counts.get(status, 0)
            for status in STATUSES
        },

        "by_priority": {
            priority: priority_counts.get(priority, 0)
            for priority in PRIORITIES
        },
    }


def print_report(report):
    """Print the ticket report."""

    print(f"Total tickets: {report['total']}")

    print("By status:")

    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("By priority:")

    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")