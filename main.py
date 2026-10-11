from campusflow.tickets import create_ticket, get_ticket
from campusflow.workflow import assign_ticket, change_status, get_work_queue
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import build_report, print_report

DATA_FILE = "data/tickets.json"


def ask_ticket_details():
    title = input("Problem title: ").strip()
    category = input("Category (Network/Hardware/Software/Other): ").strip()
    urgency = input("Urgency (low/medium/high): ").strip()
    affected_users = input("Number of affected users: ").strip()

    try:
        affected_users = int(affected_users)
    except ValueError:
        raise ValueError("Affected users must be a whole number.")

    return title, category, urgency, affected_users


def show_ticket(ticket):
    for key, value in ticket.items():
        print(f"{key}: {value}")


def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Fix the ticket file before restarting. Saved data was not replaced.")
        return

    print("Welcome to CampusFlow!")

    while True:
        print("""
--- CampusFlow Menu ---
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Change ticket status / reopen
6. Show work queue
7. Show reports
0. Exit
""")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title, category, urgency, affected_users = ask_ticket_details()

                ticket = create_ticket(
                    tickets, title, category, urgency, affected_users
                )

                save_tickets(tickets, DATA_FILE)
                print(f"Ticket created successfully: {ticket['id']}")

            elif choice == "2":
                if not tickets:
                    print("No tickets have been created.")
                else:
                    for ticket in tickets:
                        print("-" * 30)
                        show_ticket(ticket)

            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip().upper()
                ticket = get_ticket(tickets, ticket_id)

                if ticket is None:
                    print("Ticket not found.")
                else:
                    show_ticket(ticket)

            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip().upper()
                staff_name = input("Staff member name: ").strip()

                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets, DATA_FILE)

                print("Ticket assigned successfully.")

            elif choice == "5":
                ticket_id = input("Ticket ID: ").strip().upper()

                new_status = input(
                    "New status (open/in_progress/resolved): "
                ).strip().lower()

                change_status(tickets, ticket_id, new_status)
                save_tickets(tickets, DATA_FILE)

                print(f"Ticket status changed to {new_status}.")

            elif choice == "6":
                queue = get_work_queue(tickets)

                if not queue:
                    print("There are no unresolved tickets in the work queue.")
                else:
                    for ticket in queue:
                        print(
                            f"{ticket['id']} | {ticket['priority']} | "
                            f"{ticket['status']} | {ticket['title']}"
                        )

            elif choice == "7":
                print_report(build_report(tickets))

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid menu option. Choose one of the listed options.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()