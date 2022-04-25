from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from ticket.forms import ChiefForm, OperatorForm, EngineerForm
from ticket.models import Ticket
from django.urls import reverse


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'chief_tickets'


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/create.html'

    def get_form(self, form_class=None):
        user = self.request.user
        group = self.request.user.groups.get(user=user)
        operators = Group.objects.filter(name='operators')
        chiefs = Group.objects.filter(name='chiefs')
        engineers = Group.objects.filter(name='engineers')
        if group in chiefs:
            self.form_class = ChiefForm
        elif group in operators:
            self.form_class = OperatorForm
        elif group in engineers:
            self.form_class = EngineerForm
        return super().get_form()

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})


class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket/detail.html'
    context_object_name = 'chief_ticket'


class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'chief_ticket'

    def get_form(self, form_class=None):
        user = self.request.user
        group = self.request.user.groups.get(user=user)
        operators = Group.objects.filter(name='operators')
        chiefs = Group.objects.filter(name='chiefs')
        engineers = Group.objects.filter(name='engineers')
        if group in chiefs:
            self.form_class = ChiefForm
        elif group in operators:
            self.form_class = OperatorForm
        elif group in engineers:
            self.form_class = EngineerForm
        return super().get_form()

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})
