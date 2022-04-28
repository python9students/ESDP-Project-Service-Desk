from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from ticket.forms import ChiefForm, OperatorForm, EngineerForm, TicketCancelForm
from ticket.models import Ticket, TicketStatus
from django.urls import reverse


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'tickets'


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
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_canceled = False
        if str(self.object.status) == 'Отмененный':
            ticket_canceled = True
        context['ticket_canceled'] = ticket_canceled
        print(ticket_canceled)
        return context


class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'ticket'

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


class TicketCancelView(UpdateView):
    model = Ticket
    template_name = 'ticket/cancel.html'
    form_class = TicketCancelForm

    def get(self, request, *args, **kwargs):
        if str(self.get_object().status) == 'Отмененный':
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.status = TicketStatus.objects.get(name='Отмененный')
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})
