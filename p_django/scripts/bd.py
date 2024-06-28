import os
import django
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

def populate_tickets():
    from pointBank.models import Ticket 

    routes = [
        "Самара", 
        "Оренбург", 
        "Колтубановский", 
        "Тоцкое", 
        "Сорочинск"
    ]
    start_date = datetime(2024, 6, 25)
    end_date = datetime(2024, 7, 30)
    delta = timedelta(days=1)

    current_date = start_date
    tickets_to_create = []

    while current_date <= end_date:
        for route in routes:
            ticket = Ticket(
                departure=make_aware(current_date), 
                arrival=make_aware(current_date + timedelta(hours=3)), 
                from_location="Бузулук",
                to_location=route
            )
            tickets_to_create.append(ticket)
        current_date += delta

    Ticket.objects.bulk_create(tickets_to_create)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p_django.settings")
    django.setup()
    populate_tickets()
