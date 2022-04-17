from django.db import models

from ticket.views.validators import OptionalSchemeURLValidator


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
    website = models.URLField(max_length=255, blank=True, validators=[OptionalSchemeURLValidator], verbose_name='Вебсайт')
    type = models.ForeignKey('ticket.CompanyType', on_delete=models.PROTECT, verbose_name='Тип компании',
                             related_name='clients')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    country = models.ForeignKey('ticket.Country', on_delete=models.PROTECT, verbose_name='Страна',
                                related_name='clients')
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
    city = models.ForeignKey('ticket.City', on_delete=models.PROTECT, verbose_name='Город',
                             related_name='service_objects')

    def __str__(self):
        return f'{self.serial_number}'

    class Meta:
        verbose_name = 'Объект обслуживания'
        verbose_name_plural = 'Объекты обслуживания'
        db_table = 'service_object'
