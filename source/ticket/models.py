from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models

User = get_user_model()


class CompanyType(models.Model):
    """
    Модель создания типов компаний(клиентов)
    """
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип компании'
        verbose_name_plural = 'Типы компаний'
        db_table = 'company_type'


class ServiceObjectType(models.Model):
    """
    Модель для создания типов объектов обслуживания
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип объекта обслуживания'
        verbose_name_plural = 'Типы объектов обслуживания'
        db_table = 'service_object_type'


class ServiceObjectModel(models.Model):
    """
    Модель для создания моделей объектов обслуживания
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель объекта обслуживания'
        verbose_name_plural = 'Модели объектов обслуживания'
        db_table = 'service_object_model'


class Country(models.Model):
    """
    Модель для создания стран
    """
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        db_table = 'country'


class Region(models.Model):
    """
    Модель для создания стран
    """
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'
        db_table = 'region'


class City(models.Model):
    """
    Модель для создания городов
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.ForeignKey('ticket.Country', on_delete=models.CASCADE, verbose_name='Страна',
                                related_name='cities')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        db_table = 'city'


class Client(models.Model):
    """
    Модель для создания клиентов(компаний)
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    short_name = models.CharField(max_length=50, verbose_name='Сокращенное название')
    website = models.URLField(max_length=255, blank=True, validators=[
        RegexValidator(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')],
                              verbose_name='Вебсайт')
    type = models.ForeignKey('ticket.CompanyType', on_delete=models.PROTECT, verbose_name='Тип компании',
                             related_name='clients')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    country = models.ForeignKey('ticket.Country', on_delete=models.PROTECT, verbose_name='Страна',
                                related_name='clients')
    region = models.ForeignKey('ticket.Region', on_delete=models.PROTECT, verbose_name='Область', related_name='clients')
    city = models.ForeignKey('ticket.City', on_delete=models.PROTECT, verbose_name='Город', related_name='clients')


    def __str__(self):
        return f'{self.short_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        db_table = 'client'


class ServiceObject(models.Model):
    """
    Модель для создания объектов обслуживания
    """
    serial_number = models.CharField(max_length=255, unique=True, verbose_name='Серийный номер')
    model = models.ForeignKey('ticket.ServiceObjectModel', on_delete=models.PROTECT, verbose_name='Модель',
                              related_name='service_objects')
    client = models.ForeignKey('ticket.Client', on_delete=models.PROTECT, verbose_name='Клиент',
                               related_name='service_objects')
    type = models.ForeignKey('ticket.ServiceObjectType', on_delete=models.PROTECT,
                             verbose_name='Тип объекта обслуживания', related_name='service_objects')
    is_installed = models.BooleanField(default=False, verbose_name='Установлен')
    active_from = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Действителен с')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    country = models.ForeignKey('ticket.Country', on_delete=models.PROTECT, verbose_name='Страна',
                                related_name='service_objects')
    region = models.ForeignKey('ticket.Region', on_delete=models.PROTECT, verbose_name='Область', related_name='service_objects')
    city = models.ForeignKey('ticket.City', on_delete=models.PROTECT, verbose_name='Город',
                             related_name='service_objects')

    def __str__(self):
        return f'{self.serial_number}'

    class Meta:
        verbose_name = 'Объект обслуживания'
        verbose_name_plural = 'Объекты обслуживания'
        db_table = 'service_object'


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


class EmployeePosition(models.Model):
    """
    Модель для создания должностей
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должность'
        db_table = 'employee_position'


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


class ServiceLevel(models.Model):
    """
    Модель для создания уровней обслуживания
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Уровень обслуживания'
        verbose_name_plural = 'Уровни обслуживания'
        db_table = 'service_level'


class Department(models.Model):
    """
    Модель для создания департаментов
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        db_table = 'department'


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
    recieved_at = models.DateTimeField(null=True, default=None, verbose_name='Дата получения заявки')
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
    work_started_at = models.DateTimeField(null=True, default=None, verbose_name='Дата начала работ')
    work_finished_at = models.DateTimeField(null=True, default=None, verbose_name='Дата окончания работ')
    ride_started_at = models.DateTimeField(null=True, default=None, verbose_name='Дата начала поездки')
    ride_finished_at = models.DateTimeField(null=True, default=None, verbose_name='Дата окончания поездки')
    cancel_reason = models.CharField(max_length=255, verbose_name='Причина отмены заявки')

    def __str__(self):
        return f'ticket №{self.id}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        db_table = 'ticket'
        permissions = [("see_engineer_tickets",
                        "Может видеть только заявки со статусами Назначенный, На исполнении, Заверщенный"),
                       ("see_operator_tickets",
                        "Может видеть только заявки со статусами Неопределенный, Подготовленный"),
                       ("see_chief_tickets",
                        "Может видеть только заявки со статусами Подготовленный, Назначенный, Завершенный, Отмененный, На исполнении"),
                       ("close_ticket", "Может закрывать заявки")]
