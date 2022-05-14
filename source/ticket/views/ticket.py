from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from datetime import date, datetime, timedelta

from ticket.forms import ChiefForm, EngineerForm, TicketCancelForm
from ticket.models import Ticket, TicketStatus, ServiceObject
from django.urls import reverse


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'tickets'
    ordering = ['-created_at']

    def get_queryset(self):
        tickets = super().get_queryset()
        if self.request.user.has_perm('ticket.see_engineer_tickets') and not self.request.user.is_superuser:
            return tickets.filter(status__in=[2, 6, 7]).filter(executor=self.request.user)
        elif self.request.user.has_perm('ticket.see_chief_tickets') and not self.request.user.is_superuser:
            return tickets.filter(status__in=[1, 2, 3, 4, 5, 6, 7])
        return tickets


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/create.html'

    def form_valid(self, form):
        instance = form.save()
        instance.operator = self.request.user
        instance.status = TicketStatus.objects.get(name='Подготовленный')
        return super(TicketCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        user = self.request.user
        group = self.request.user.groups.get(user=user)
        chiefs = Group.objects.filter(name='chiefs')
        engineers = Group.objects.filter(name='engineers')
        admins = Group.objects.filter(name='admins')
        if group in chiefs or admins:
            self.form_class = ChiefForm
        elif group in engineers:
            self.form_class = EngineerForm
        return super().get_form()

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs['service_objects'] = list(ServiceObject.objects.all().values('id', 'serial_number', 'client_id'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})

    def get(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.get(user=user)
        engineers = Group.objects.filter(name='engineers')
        if group in engineers:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'ticket/detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_canceled = False
        is_chief = False
        user = self.request.user
        group = user.groups.get(user=user)
        chiefs = Group.objects.filter(name='chiefs')
        service_objects = ServiceObject.objects.filter(pk=self.object.service_object_id)
        expected_time_to_fix_problem = None
        for service_object in service_objects:
            for contract in service_object.contracts.all():
                expected_time_to_fix_problem = self.object.recieved_at + contract.time_to_fix_problem_SLA
        if expected_time_to_fix_problem is not None:
            remaining_time_to_fix_problem = expected_time_to_fix_problem - datetime.now().replace(tzinfo=timezone.utc)
            if remaining_time_to_fix_problem.days < 0:
                context['remaining_time_to_fix_problem'] = None
            else:
                context['remaining_time_to_fix_problem'] = remaining_time_to_fix_problem
        if group in chiefs:
            is_chief = True
        if str(self.object.status) == 'Отмененный':
            ticket_canceled = True
        context['ticket_canceled'] = ticket_canceled
        context['is_chief'] = is_chief
        context['expected_time_to_fix_problem'] = expected_time_to_fix_problem
        return context


class TicketUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'ticket'
    permission_required = 'ticket.change_ticket'

    def get_form(self, form_class=None):
        user = self.request.user
        group = self.request.user.groups.get(user=user)
        chiefs = Group.objects.filter(name='chiefs')
        engineers = Group.objects.filter(name='engineers')
        if group in chiefs:
            self.form_class = ChiefForm
        elif group in engineers:
            self.form_class = EngineerForm
        return super().get_form()

    def form_valid(self, form):
        if self.object.executor and self.object.driver and not self.object.ride_started_at:
            self.object.status = TicketStatus.objects.get(name='Назначенный')
        elif self.object.ride_started_at:
            self.object.status = TicketStatus.objects.get(name='На исполнении')
            self.object.save()
        if self.object.ride_started_at and self.object.work_started_at and \
                self.object.work_finished_at and self.object.ride_finished_at:
            self.object.status = TicketStatus.objects.get(name='Исполненный')
            self.object.save()
        if 'close_ticket' in self.request.POST:
            self.object = form.save(commit=False)
            self.object.status = TicketStatus.objects.get(name="Завершенный")
            self.object.closed_at = timezone.now()
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["form"].fields['service_object'].queryset = self.object.client.service_objects.all()
        kwargs['service_objects'] = list(ServiceObject.objects.all().values('id', 'serial_number', 'client_id'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})


class TicketCancelView(UpdateView):
    model = Ticket
    template_name = 'ticket/cancel.html'
    form_class = TicketCancelForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.get(user=user)
        chiefs = Group.objects.filter(name='chiefs')
        if group not in chiefs:
            raise PermissionDenied
        if str(self.get_object().status) == 'Отмененный':
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.status = TicketStatus.objects.get(name='Отмененный')
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.object.pk})
