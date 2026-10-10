ticket = {
    "id": "T001"
    "title": "campus wifi is down"
    "category": "network"
    "urgency": "high"
    "affected user": "15"
    "status": "critical"
    "status": "open"
    "assign to": none
}
import json
from pathlib import path
def save_tickets(tickets, file_path="data/tickes.json"):
    path = path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(tickes, file, indent_4)