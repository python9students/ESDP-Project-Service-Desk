from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from accounts.views import User
from ticket.forms import ChiefForm, OperatorForm
from ticket.models import Ticket
from django.urls import reverse


class ChiefTicketListView(ListView):
    model = Ticket
    template_name = 'chief/list.html'
    context_object_name = 'chief_tickets'


class ChiefTicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'chief/create.html'

    def get_form(self, form_class=None):
        user = User.objects.get(pk=self.request.user.id)
        group = Group.objects.get(name='operators')
        if self.request.user.is_superuser:
            self.form_class = ChiefForm
        elif group in self.request.user.groups.all():
            self.form_class = OperatorForm
        elif self.request.user.is_staff:
            self.form_class = ChiefForm
        else:
            self.form_class = OperatorForm
        return super().get_form()

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

    def get_form(self, form_class=None):
        user = User.objects.get(pk=self.request.user.id)
        group = Group.objects.get(name='operators')
        if self.request.user.is_superuser:
            self.form_class = ChiefForm
        elif group in self.request.user.groups.all():
            self.form_class = OperatorForm
        elif self.request.user.is_staff:
            self.form_class = ChiefForm
        else:
            self.form_class = OperatorForm
        return super().get_form()

    def get_success_url(self):
        return reverse("ticket:chief_ticket_detail", kwargs={"pk": self.object.pk})
