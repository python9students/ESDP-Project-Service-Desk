from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from forms import EngineerForm
from ticket.models import Ticket


class EngineerTicketListView(ListView):
    model = Ticket
    template_name = 'engineer/list.html'
    context_object_name = 'tickets'


class EngineerTicketDetailView(DetailView):
    template_name = 'engineer/detail.html'
    model = Ticket


class EngineerTicketCreateView(CreateView):
    model = Ticket
    form_class = EngineerForm
    template_name = "engineer/create.html"

    def get_success_url(self):
        return reverse("ticket:engineer_ticket_view", kwargs={"pk": self.object.pk})


class EngineerTicketUpdateView(UpdateView):
    model = Ticket
    form_class = EngineerForm
    template_name = "engineer/update.html"

    def get_success_url(self):
        return reverse("ticket:engineer_ticket_view", kwargs={"pk": self.object.pk})
