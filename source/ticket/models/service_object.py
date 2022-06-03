from django.db import models


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
    region = models.ForeignKey('ticket.Region', on_delete=models.PROTECT, verbose_name='Область',
                               related_name='service_objects')
    city = models.ForeignKey('ticket.City', on_delete=models.PROTECT, verbose_name='Город',
                             related_name='service_objects')
    criterion = models.ForeignKey('ticket.CriterionType', on_delete=models.PROTECT, verbose_name='Критерий',
                                  related_name='service_objects', null=True, default="Гарантийный")
    guarantee_valid_from = models.DateField(blank=True, null=True, verbose_name='Гарантия действует с')
    guarantee_valid_until = models.DateField(blank=True, null=True, verbose_name='Гарантия действует до')
    time_to_fix_problem = models.DurationField(verbose_name='Время на устранение проблемы', null=True, blank=True,
                                               default=None)

    def __str__(self):
        return f'{self.serial_number}'

    class Meta:
        verbose_name = 'Объект обслуживания'
        verbose_name_plural = 'Объекты обслуживания'
        db_table = 'service_object'


class CriterionType(models.Model):
    """
    Модель для создания критерия
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'
        db_table = 'criterion_type'


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
