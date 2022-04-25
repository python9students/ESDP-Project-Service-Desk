from django.views.generic import CreateView, ListView, DetailView, UpdateView
from ticket.forms import ChiefForm
from ticket.models import Ticket
from django.urls import reverse


class ChiefTicketListView(ListView):
    model = Ticket
    template_name = 'chief/list.html'
    context_object_name = 'chief_tickets'


class ChiefTicketCreateView(CreateView):
    model = Ticket
    template_name = 'chief/create.html'
    form_class = ChiefForm

    def get_success_url(self):
        return reverse("ticket:chief_ticket_detail", kwargs={"pk": self.object.pk})


class ChiefTicketDetailView(DetailView):
    model = Ticket
    template_name = 'chief/detail.html'
    context_object_name = 'chief_ticket'


class ChiefTicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'chief/update.html'
    context_object_name = 'chief_ticket'
    form_class = ChiefForm

    def get_success_url(self):
        return reverse("ticket:chief_ticket_detail", kwargs={"pk": self.object.pk})
