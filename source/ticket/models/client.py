from django.db import models
from django.core.validators import RegexValidator


class Client(models.Model):
    """
    Модель для создания клиентов(компаний)
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    short_name = models.CharField(max_length=50, verbose_name='Сокращенное название')
    website = models.URLField(max_length=255, blank=True, validators=[
        RegexValidator(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')],
                              verbose_name='Вебсайт')
    email = models.EmailField(verbose_name='E-mail')
    type = models.ForeignKey('ticket.CompanyType', on_delete=models.PROTECT, verbose_name='Тип компании',
                             related_name='clients')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    country = models.ForeignKey('ticket.Country', on_delete=models.PROTECT, verbose_name='Страна',
                                related_name='clients')
    region = models.ForeignKey('ticket.Region', on_delete=models.PROTECT, verbose_name='Область',
                               related_name='clients')
    city = models.ForeignKey('ticket.City', on_delete=models.PROTECT, verbose_name='Город', related_name='clients')

    def __str__(self):
        return f'{self.short_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        db_table = 'client'


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
