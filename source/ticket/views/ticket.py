from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.db.models import Q
from ticket.filters import TicketFilter
from ticket.forms import ChiefForm, EngineerForm, TicketCancelForm, TicketCloseForm
from django.urls import reverse

from ticket.models.service_object import ServiceObject
from ticket.models.ticket import Ticket, TicketStatus, Work, ProblemArea
from ticket.views.ticket_custom_datetime_functions import buisnesstimedelta_function

User = get_user_model()


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'tickets'
    paginate_by = 10
    paginate_orphans = 0
    ordering = ['-received_at']

    def get_queryset(self):
        tickets = super().get_queryset()
        if self.request.user.has_perm('ticket.see_engineer_tickets') and not self.request.user.is_superuser:
            return tickets.filter(status__in=[2, 6, 7]).filter(executor=self.request.user)
        return TicketFilter(self.request.GET, queryset=tickets).qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['filter'] = TicketFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/create.html'

    def form_valid(self, form):
        instance = form.save()
        instance.operator = self.request.user
        instance.status = TicketStatus.objects.get(name='Подготовленный')
        return super(TicketCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        admin_group = Group.objects.get(name='admins')
        chief_group = Group.objects.get(name='chiefs')
        engineer_group = Group.objects.get(name='engineers')
        if chief_group in self.request.user.groups.all() or admin_group in self.request.user.groups.all():
            self.form_class = ChiefForm
        elif engineer_group in self.request.user.groups.all():
            self.form_class = EngineerForm
        return super().get_form()

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs['service_objects'] = list(ServiceObject.objects.all().values('id', 'serial_number', 'client_id'))
        kwargs['works'] = Work.objects.all()
        kwargs['problem_areas'] = ProblemArea.objects.all()

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
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        ticket_canceled = False
        ticket_closed = False
        is_chief = False
        user = self.request.user
        group = user.groups.get(user=user)
        chiefs = Group.objects.filter(name='chiefs')
        if group in chiefs:
            is_chief = True
        if str(self.object.status) == 'Отмененный':
            ticket_canceled = True
        if str(self.object.status) == 'Завершенный':
            ticket_closed = True
        if ticket.expected_finish_date:
            '''Устанавливаю правило рабочего дня чтобы получить разницу между начальным и финальнымы днями'''
            time_difference = buisnesstimedelta_function(ticket)
            expected_time_to_finish = ticket.expected_finish_date
            context['time_difference'] = time_difference.hours
            context['expected_time_to_finish'] = expected_time_to_finish
        context['ticket_canceled'] = ticket_canceled
        context['ticket_closed'] = ticket_closed
        context['is_chief'] = is_chief
        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'ticket'

    def get_form(self, form_class=None):
        admin_group = Group.objects.get(name='admins')
        chief_group = Group.objects.get(name='chiefs')
        engineer_group = Group.objects.get(name='engineers')
        if chief_group in self.request.user.groups.all() or admin_group in self.request.user.groups.all():
            self.form_class = ChiefForm
        elif engineer_group in self.request.user.groups.all():
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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["form"].fields['service_object'].queryset = self.object.client.service_objects.all()
        kwargs['service_objects'] = list(ServiceObject.objects.all().values('id', 'serial_number', 'client_id'))
        kwargs['works'] = Work.objects.all()
        kwargs['problem_areas'] = ProblemArea.objects.all()
        return super().get_context_data(**kwargs)


class TicketCancelView(UpdateView):
    model = Ticket
    template_name = 'ticket/cancel.html'
    form_class = TicketCancelForm

    def get(self, request, *args, **kwargs):
        chief_group = Group.objects.get(name='chiefs')
        if chief_group not in self.request.user.groups.all():
            raise PermissionDenied
        if str(self.get_object().status) == 'Отмененный':
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.status = TicketStatus.objects.get(name='Отмененный')
        self.object.save()
        return super().form_valid(form)


class TicketCloseView(UpdateView):
    model = Ticket
    template_name = 'ticket/close.html'
    form_class = TicketCloseForm

    def get(self, request, *args, **kwargs):
        chief_group = Group.objects.get(name='chiefs')
        if chief_group not in self.request.user.groups.all():
            raise PermissionDenied
        if str(self.get_object().status) == 'Завершенный':
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.status = TicketStatus.objects.get(name='Завершенный')
        self.object.save()
        return super().form_valid(form)


class ChiefInfoDetailView(ListView):
    model = Ticket
    template_name = 'for_chief/chief_info_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets_driver = Ticket.objects.values('driver')
        usernames = User.objects.filter(id__in=tickets_driver).values('id', 'last_name', 'first_name')
        tickets = Ticket.objects.filter((Q(status__name="На исполнении") | Q(status__name='Назначенный')))
        print(tickets_driver)
        print(usernames)
        context['tickets'] = tickets
        context['tickets_driver'] = tickets_driver
        context['usernames'] = usernames
        return context
