from django.db import models

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
        unique_together = ('name',)


class Region(models.Model):
    """
    Модель для создания стран
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.ForeignKey('ticket.Country', on_delete=models.CASCADE, verbose_name='Страна',
                                related_name='regions')

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