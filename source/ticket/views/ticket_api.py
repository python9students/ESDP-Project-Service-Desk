from datetime import datetime, timezone
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ticket.models import ServiceObject, Ticket


class TicketTimeView(View):
    def get(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs.get('pk'))
        service_object = ServiceObject.objects.get(serial_number=ticket.service_object)
        time_to_fix_problem = service_object.time_to_fix_problem
        expected_time_to_finish_work = ticket.received_at + time_to_fix_problem
        return JsonResponse(
            {"ticket_received_at": ticket.received_at,
             "expected_time_to_finish_work": expected_time_to_finish_work,
             "date_time_now": datetime.now(),
             }
        )

