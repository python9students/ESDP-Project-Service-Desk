from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
import datetime, businesstimedelta, pytz

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()


class Ticket(models.Model):
    """
    Модель для создания заявок(тикетов)
    """
    client = models.ForeignKey('ticket.Client', on_delete=models.PROTECT, verbose_name='Клиент',
                               related_name='tickets', null=True, default=None)
    service_object = models.ForeignKey('ticket.ServiceObject', on_delete=models.PROTECT,
                                       verbose_name='Объект обслуживания', related_name='tickets', null=True,
                                       default=None)
    priority = models.ForeignKey('ticket.TicketPriority', on_delete=models.PROTECT, verbose_name='Приоритет',
                                 related_name='tickets', null=True, default=None)
    type = models.ForeignKey('ticket.TicketType', on_delete=models.PROTECT, verbose_name='Тип заявки',
                             related_name='tickets', null=True, default=None)
    status = models.ForeignKey('ticket.TicketStatus', on_delete=models.PROTECT, verbose_name='Статус заявки',
                               related_name='tickets', null=True, default=4)
    service_level = models.ForeignKey('ticket.ServiceLevel', on_delete=models.PROTECT,
                                      verbose_name='Уровень обслуживания', related_name='tickets',
                                      null=True, default=None)
    department = models.ForeignKey('ticket.Department', on_delete=models.PROTECT, verbose_name='Департамент',
                                   related_name='tickets', null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения заявки")
    received_at = models.DateTimeField(null=True, default=None, verbose_name='Дата получения заявки')
    desired_to = models.DateTimeField(null=True, default=None, verbose_name='Желаемая дата исполнения')
    operator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Оператор',
                                 related_name='operator_tickets', null=True)
    works = models.ManyToManyField('ticket.Work', related_name='tickets')
    problem_areas = models.ManyToManyField('ticket.ProblemArea', related_name='tickets')
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Исполнитель',
                                 related_name='executor_tickets', null=True, default=None)
    driver = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Водитель', related_name='driver_tickets',
                               null=True, default=None)
    closed_at = models.DateTimeField(null=True, default=None, verbose_name='Дата закрытия заявки')
    ride_started_at = models.DateTimeField(null=True, default=None, verbose_name='Дата начала поездки')
    work_started_at = models.DateTimeField(null=True, default=None, verbose_name='Дата начала работ')
    work_finished_at = models.DateTimeField(null=True, default=None, verbose_name='Дата окончания работ')
    ride_finished_at = models.DateTimeField(null=True, default=None, verbose_name='Дата окончания поездки')
    cancel_reason = models.CharField(max_length=255, verbose_name='Причина отмены заявки')
    close_commentary = models.CharField(max_length=255, blank=True, verbose_name='Комментарий к закрытию заявки')
    work_done = models.TextField(max_length=1000, blank=True, verbose_name='Проделанная работа')
    expected_finish_date = models.DateTimeField(null=True, default=None, verbose_name='Ожидаемая дата завершения')

    def __str__(self):
        return f'Заявка-{self.received_at.strftime("%Y%m%d-%H%M%S")}'

    def get_absolute_url(self):
        return reverse('ticket:ticket_detail', kwargs={'pk': self.pk})

    @property
    def buisnesstimedelta_function(self):
        if self.expected_finish_date:
            workday = businesstimedelta.WorkDayRule(
                start_time=datetime.time(9),
                end_time=datetime.time(18),
                working_days=[0, 1, 2, 3, 4],
                tz=pytz.timezone('Asia/Bishkek'))
            businesshrs = businesstimedelta.Rules([workday])
            time_difference = businesshrs.difference(datetime.datetime.now(), self.expected_finish_date)
            return time_difference.hours
        else:
            return ""

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        db_table = 'ticket'
        permissions = [("see_engineer_tickets",
                        "Может видеть только заявки со статусами Назначенный, На исполнении, Исполненный"),
                       ("see_chief_tickets",
                        "Может видеть заявки со всеми статусами"),
                       ("close_ticket", "Может закрывать заявки")]


class TicketPriority(models.Model):
    """
    Модель для создания приоритетов Заявки
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Приоритет заявки'
        verbose_name_plural = 'Приоритеты заявок'
        db_table = 'ticket_priority'


class TicketType(models.Model):
    """
    Модель для создания типов Заявки
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'
        db_table = 'ticket_type'


class TicketStatus(models.Model):
    """
    Модель для создания статусов Заявки
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
        db_table = 'ticket_status'


class Work(MPTTModel):
    """
    Модель для создания работ используя древовидную структуру
    """
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        db_table = 'work'


class ProblemArea(MPTTModel):
    """
    Модель для создания проблемных областей используя древовидную структуру
    """
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Проблемная область'
        verbose_name_plural = 'Проблемные области'
        db_table = 'problem_area'
