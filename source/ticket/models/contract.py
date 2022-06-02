from django.db import models


class Contract(models.Model):
    """
    Модель для создания договоров
    """
    doc_number = models.CharField(max_length=50, verbose_name='№ Документа')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    type = models.ForeignKey('ticket.ContractType', on_delete=models.PROTECT, verbose_name='Тип договора',
                             related_name='contracts')
    department = models.ForeignKey('ticket.Department', on_delete=models.PROTECT, verbose_name='Департамент',
                                   related_name='contracts')
    company_client = models.ForeignKey('ticket.Client', on_delete=models.PROTECT, verbose_name='Компания-клиент',
                                       related_name='contracts')
    valid_from = models.DateField(verbose_name='Действует с')
    valid_until = models.DateField(verbose_name='Действует до')
    status = models.ForeignKey('ticket.ContractStatus', on_delete=models.PROTECT, verbose_name='Статус',
                               related_name='contracts')

    def __str__(self):
        return f'{self.doc_number}'

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'
        db_table = 'contract'


class ContractFiles(models.Model):
    contract = models.ForeignKey(
        "ticket.Contract", on_delete=models.CASCADE, related_name="contract_files"
    )
    current_document = models.FileField(upload_to='contracts', verbose_name='Действующий документ')

    def __str__(self):
        return f'{self.current_document}'

    class Meta:
        verbose_name = 'Действующий документ'
        verbose_name_plural = 'Действующие документы'
        db_table = 'contract_files'


class ContractType(models.Model):
    """
    Модель для создания типов Договора
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип договора'
        verbose_name_plural = 'Типы договоров'
        db_table = 'contract_type'


class ContractStatus(models.Model):
    """
    Модель для создания статусов Договора
    """
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус договора'
        verbose_name_plural = 'Статусы договоров'
        db_table = 'contract_status'
