from datetime import datetime
from django.http import JsonResponse
from django.views import View

from ticket.models import Ticket, ServiceObject


class TicketTimeView(View):
    def get(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs.get('pk'))
        expected_time_to_finish_work = ticket.expected_finish_date

        return JsonResponse(
            {"ticket_received_at": ticket.received_at,
             "expected_time_to_finish_work": expected_time_to_finish_work,
             "date_time_now": datetime.now(),
             }
        )


class ServiceObjectDetailView(View):
    def get(self, *args, **kwargs):
        service_object = ServiceObject.objects.get(id=self.kwargs.get('pk'))
        time_to_finish = service_object.time_to_fix_problem

        return JsonResponse(
            {"time_to_finish": str(time_to_finish)}
        )
