from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from ticket.forms import ChiefForm, OperatorForm, EngineerForm
from ticket.models import Ticket, TicketStatus
from django.urls import reverse
from datetime import datetime


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'chief_tickets'


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/create.html'

    def get_form_kwargs(self):
        res = super(TicketCreateView, self).get_form_kwargs()
        if self.form_class == OperatorForm:
            res['initial']['operator'] = self.request.user
        return res

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
        else:
            self.form_class = ChiefForm
        return super().get_form()

    def form_valid(self, form):
        status = TicketStatus.objects.get(name="Завершенный")
        if 'close_ticket' in self.request.POST:
            self.object = form.save(commit=False)
            self.object.status = status
            self.object.closed_at = timezone.now()
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})
