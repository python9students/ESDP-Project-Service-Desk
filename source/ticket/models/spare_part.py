from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SparePart(models.Model):
    """
    Модель для добавления Запчастей
    """
    SPARE_PART_CHOICES = [('pc', 'шт'), ('unit', 'узел')]

    serial_number = models.CharField(max_length=100, unique=True, verbose_name='Серийный №')
    name = models.CharField(max_length=100, verbose_name='Название')
    product_code = models.CharField(max_length=100, verbose_name='Код продукта')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    measure_unit = models.CharField(max_length=20, choices=SPARE_PART_CHOICES, default='шт',
                                    verbose_name='Единица измерения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления запчасти")
    condition = models.ForeignKey('ticket.Condition', on_delete=models.CASCADE, verbose_name='Состояние запчасти')
    supplier_company = models.ForeignKey('ticket.SupplierCompany', on_delete=models.CASCADE,
                                         verbose_name='Компания поставщик')
    engineers = models.ManyToManyField(User, related_name='spare_parts', through='SparePartUser',
                                       through_fields=('spare_part', 'engineer'))

    def __str__(self):
        return f'{self.name}, {self.serial_number}'

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        db_table = 'spare_part'


class Condition(models.Model):
    name = models.CharField(max_length=50, verbose_name='Состояние')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Состояние запчасти'
        verbose_name_plural = 'Состояние запчастей'
        db_table = 'spare_part_condition'


class SupplierCompany(models.Model):
    name = models.CharField(max_length=50, verbose_name='Компания поставщик')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Компания поставщик'
        verbose_name_plural = 'Компании поставщики'
        db_table = 'spare_part_supplier_company'


class SparePartUser(models.Model):
    SPARE_PART_STATUS_CHOICES = [('assigned', 'Назначенный'), ('set', 'Установленный'),
                                 ('returned', 'Возвращенный')]

    spare_part = models.ForeignKey('ticket.SparePart', on_delete=models.PROTECT, verbose_name='Запчасть')
    engineer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Назначить на')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата назначения запчасти")
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Назначен кем',
                                    related_name='assigned_spare_parts')
    ticket = models.ForeignKey('ticket.Ticket', null=True, on_delete=models.PROTECT, verbose_name='Заявка')
    service_object = models.ForeignKey('ticket.ServiceObject', null=True, on_delete=models.PROTECT,
                                       verbose_name='Сервисный объект')
    status = models.CharField(max_length=20, choices=SPARE_PART_STATUS_CHOICES, default='assigned',
                              verbose_name='Статус')

    def __str__(self):
        return f'{self.engineer} - {self.spare_part.name} - {self.quantity}'

    class Meta:
        verbose_name = 'Передача запчасти инженеру'
        verbose_name_plural = 'Передача запчастей инженеру'
        db_table = 'Spare_part_user'
        permissions = [("see_engineer_spare_parts",
                        "Может видеть только запчасти со статусами Назначенный, Установленный")]
