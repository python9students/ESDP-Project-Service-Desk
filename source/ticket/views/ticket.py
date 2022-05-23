import businesstimedelta
import pytz
from dateutil.tz import tz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView
import datetime
from pytz import timezone
from ticket.filters import TicketFilter
from ticket.forms import ChiefForm, EngineerForm, TicketCancelForm, TicketCloseForm
from ticket.models import Ticket, TicketStatus, ServiceObject
from django.urls import reverse

from ticket.views.ticket_custom_datetime_functions import find_working_day_after, convert_hour_to_sec, \
    add_weekday_seconds


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    context_object_name = 'tickets'
    paginate_by = 2
    paginate_orphans = 0
    ordering = ['-received_at']

    def get_queryset(self):
        tickets = super().get_queryset()
        if self.request.user.has_perm('ticket.see_engineer_tickets') and not self.request.user.is_superuser:
            return tickets.filter(status__in=[2, 6, 7]).filter(executor=self.request.user)
        elif self.request.user.has_perm('ticket.see_chief_tickets') and not self.request.user.is_superuser:
            return tickets.filter(status__in=[1, 2, 3, 4, 5, 6, 7])
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
        UTC = timezone('Asia/Bishkek')
        received_date = tz.tzlocal()
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        service_object = ServiceObject.objects.get(serial_number=ticket.service_object)
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
        if service_object.time_to_fix_problem:
            '''Устанавливаю правило рабочего дня чтобы получить разницу между начальным и финальнымы днями'''
            workday = businesstimedelta.WorkDayRule(
                start_time=datetime.time(9),
                end_time=datetime.time(18),
                working_days=[0, 1, 2, 3, 4],)
            businesshrs = businesstimedelta.Rules([workday])

            '''Получаю из базы данных время и конвертирую его в локальное время'''
            dbdatetime = ticket.received_at.replace(tzinfo=pytz.utc)
            received_date = dbdatetime.astimezone(received_date)
            print(received_date)

            '''Получаю время у service_object за которое надо закончить работу и конвертирую его в секунды'''
            str_time_to_fix = str(service_object.time_to_fix_problem)
            seconds = convert_hour_to_sec(str_time_to_fix)
            '''Узнаю дату окончания исключая выходные'''
            ending_date = add_weekday_seconds(received_date, seconds)

            print(ending_date)

            '''Узнаю сколько рабочих часов между двумья датами исключая выходные'''
            # hours = businesshrs.difference(datetime.datetime.now(UTC).replace(microsecond=0), ending_date)
            hours = businesshrs.difference(received_date, ending_date)
            print(hours)








            expected_time_to_finish = ticket.received_at.replace(microsecond=0) + service_object.time_to_fix_problem
            time_difference = expected_time_to_finish.replace(microsecond=0) - datetime.datetime.now(UTC).replace(
                microsecond=0)




            # start_day = ticket.received_at.replace(microsecond=0)
            # days_to_add = datetime.datetime.now()



            # expected_time_to_finish_trial = find_working_day_after(start_day, days_to_add)
            # print(expected_time_to_finish_trial)




            # hours = businesshrs.difference(datetime.datetime.now(UTC).replace(microsecond=0), expected_time_to_finish)
            # print(hours)


            context['time_difference'] = time_difference
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
    context_object_name = 'tickets'

    def get_queryset(self):
        return super().get_queryset().order_by("driver", "executor").filter(status__name="Назначенный")
