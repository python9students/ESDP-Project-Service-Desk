import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.db import connection
from django.db.models.functions import Cast
from django.shortcuts import redirect
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, F, FloatField, ExpressionWrapper, IntegerField, DateTimeField, DurationField
from ticket.filters import TicketFilter
from ticket.forms import ChiefForm, EngineerForm, TicketCancelForm, TicketCloseForm
from django.urls import reverse

from ticket.models import Ticket, TicketStatus, Work, ProblemArea, ServiceObject
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
        tickets = super().get_queryset().select_related('status', 'client', 'service_object', 'priority')
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
        if self.request.user.groups.filter(Q(name='chiefs') | Q(name='admins')).exists():
            self.form_class = ChiefForm
        elif self.request.user.groups.filter(name='engineers').exists():
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
        if self.request.user.groups.filter(name='engineers').exists():
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'ticket/detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'type', 'operator', 'service_object__client', 'priority', 'service_level', 'status',
            'executor', 'driver', ).prefetch_related(
            'works', 'problem_areas').annotate(
            remaining_date=F('expected_finish_date') - datetime.datetime.now()).annotate(
            received_and_end_date=F('expected_finish_date') - F('received_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.expected_finish_date:
            context['percentage'] = self.object.remaining_date / self.object.received_and_end_date * 100
        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'ticket'

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(Q(name='chiefs') | Q(name='admins')).exists():
            self.form_class = ChiefForm
        elif self.request.user.groups.filter(name='engineers').exists():
            self.form_class = EngineerForm
        return super().get_form()

    def form_valid(self, form):
        if not self.object.status.name == 'Завершенный':
            if self.object.executor and self.object.driver and not self.object.ride_started_at:
                self.object.status = TicketStatus.objects.get(name='Назначенный')
                self.object.save()
            elif self.object.ride_started_at and self.object.executor and self.object.driver:
                self.object.status = TicketStatus.objects.get(name='На исполнении')
                self.object.save()
            elif not self.object.ride_started_at and not self.object.executor or not self.object.driver:
                self.object.status = TicketStatus.objects.get(name='Подготовленный')
                self.object.save()
            if (self.object.ride_started_at and self.object.work_started_at and
                    self.object.work_finished_at and self.object.ride_finished_at):
                self.object.status = TicketStatus.objects.get(name='Исполненный')
                self.object.save()
            return super().form_valid(form)
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

    def get_queryset(self):
        self.queryset = super().get_queryset().select_related(
            'service_object', 'operator', 'service_object__client', 'status')
        return self.queryset

    def get_object(self, queryset=None):
        return super().get_object(queryset=self.queryset)

    def get(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='chiefs').exists():
            raise PermissionDenied
        if self.get_object().status == 'Отмененный':
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

    def get_queryset(self):
        self.queryset = super().get_queryset().select_related(
            'service_object', 'operator', 'service_object__client', 'status')
        return self.queryset

    def get_object(self, queryset=None):
        return super().get_object(queryset=self.queryset)

    def get(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='chiefs').exists():
            raise PermissionDenied
        if self.get_object().status.name == 'Завершенный':
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.object.work_done:
            self.object.status = TicketStatus.objects.get(name='Завершенный')
            self.object.closed_at = timezone.now()
            self.object.save()
            send_client_email = self.request.POST.get('send_email')
            if send_client_email == 'Yes':
                context = {'ticket': self.object}
                subject = f'Отчет по работе по заявке над сервисным объектом: {self.object.service_object}'
                email_from = settings.EMAIL_HOST_USER
                recipient = self.object.client.email
                recipient_list = [recipient, ]
                message = get_template('mail/mail.html').render(context)
                msg = EmailMessage(subject, message, email_from, recipient_list)
                msg.content_subtype = 'html'
                msg.send()
        else:
            messages.info(self.request, f'У этой заявки еще не заполнены проделланные работы, отредактируйте и '
                                        f'возвращайтесь закрывать заявку')
            return redirect('ticket:ticket_update', pk=self.kwargs.get("pk"))
        return super().form_valid(form)


class ChiefInfoDetailView(ListView):
    model = Ticket
    template_name = 'for_chief/chief_info_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = Ticket.objects.select_related(
            'driver', 'priority', 'client', 'service_object', 'status', 'executor', 'service_object__city').filter(
            (Q(status__name="На исполнении") | Q(status__name='Назначенный')))
        context['tickets'] = tickets
        active_executor_tickets = Count('executor_tickets', filter=Q(
            executor_tickets__status__name__in=['Назначенный', 'На исполнении']))
        executor_users = User.objects.filter(executor_tickets__in=tickets).annotate(num_tickets=active_executor_tickets)
        context['executor_users'] = executor_users
        active_driver_tickets = Count('driver_tickets', filter=Q(
            driver_tickets__status__name__in=['Назначенный', 'На исполнении']))
        driver_users = User.objects.filter(driver_tickets__in=tickets).annotate(num_tickets=active_driver_tickets)
        context['driver_users'] = driver_users
        return context
