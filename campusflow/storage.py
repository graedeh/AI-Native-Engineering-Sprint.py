"""JSON persistence for CampusFlow tickets."""

import json
import os



def save_tickets(tickets, filename):
    """Save all tickets to a JSON file."""

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(filename):
    """Load saved tickets, or return an empty list if the file is missing."""

    with open(filename, "r", encoding="utf-8") as file:
        tickets = json.load(file)


    if not isinstance(tickets, list):
        raise ValueError(
            f"The ticket file must contain a JSON list of tickets"
        )

    return tickets