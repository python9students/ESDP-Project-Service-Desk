from django.views.generic import CreateView, ListView
from ticket.forms import ChiefForm
from ticket.models import Ticket


class ChiefTicketListView(ListView):
    model = Ticket
    template_name = 'chief/list.html'
    context_object_name = 'chief_tickets'


class ChiefTicketCreateView(CreateView):
    model = Ticket
    template_name = 'chief/create.html'
    form_class = ChiefForm