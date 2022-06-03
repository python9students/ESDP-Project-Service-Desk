import django_filters
from django.forms import DateInput, Select
from django_filters import DateFilter, ModelChoiceFilter

from ticket.models.client import Client
from ticket.models.spare_part import SparePartUser, SparePart
from ticket.models.ticket import Ticket, User, TicketStatus


class TicketFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'По возрастанию'),
        ('descending', 'По убыванию')
    )

    client = django_filters.ModelChoiceFilter(label='Клиент', queryset=Client.objects.all(),
                                              widget=Select(attrs={'class': 'form-select form-select-sm',
                                                                   'style': "width:170px; display:inline-flex;"}))
    status = django_filters.ModelChoiceFilter(label='Статус', queryset=TicketStatus.objects.all(),
                                              widget=Select(attrs={'class': 'form-select form-select-sm',
                                                                   'style': "width:170px; display:inline-flex;"}))
    start_date = DateFilter(field_name='received_at', lookup_expr='gte', label='С',
                            widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                                    'style': "width:130px; display:inline-flex;"}, format='%d/%m/%Y'))
    end_date = DateFilter(field_name='received_at', lookup_expr='lte', label='По',
                          widget=DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm',
                                                  'style': "width:130px; display:inline-flex;"}, format='%d/%m/%Y', ))
    ordering = django_filters.ChoiceFilter(label='Сортировать по', choices=CHOICES, method='sort_by_order',
                                           widget=Select(attrs={'class': 'form-select form-select-sm',
                                                                'style': "width:170px; display:inline-flex;"}))

    class Meta:
        model = Ticket
        fields = ['client', 'status']

    def sort_by_order(self, queryset, name, value):
        expression = 'received_at' if value == 'ascending' else '-received_at'
        return queryset.order_by(expression)


class SparePartUserFilter(django_filters.FilterSet):
    spare_part = django_filters.ModelChoiceFilter(label='Запчасть', queryset=SparePart.objects.all(),
                                                  widget=Select(attrs={'class': 'form-select form-select-sm',
                                                                       'style': "width:220px; display:inline-flex;"}))
    assigned_by = django_filters.ModelChoiceFilter(label='Назначена кем', queryset=User.objects.all(),
                                                   widget=Select(attrs={'class': 'form-select form-select-sm',
                                                                        'style': "width:170px; display:inline-flex;"}))
    engineer = ModelChoiceFilter(queryset=User.objects.all(), label='Назначена кому',
                                 widget=Select(attrs={'class': 'form-select form-select-sm',
                                                      'style': "width:170px; display:inline-flex;"})
                                 )
    status = django_filters.ChoiceFilter(label='Статус', choices=SparePartUser.SPARE_PART_STATUS_CHOICES,
                                         widget=Select(attrs={'class': 'form-select form-select-sm',
                                                              'style': "width:150px; display:inline-flex;"}))

    class Meta:
        model = SparePartUser
        fields = ['spare_part', 'assigned_by', 'engineer', 'status']

    def __init__(self, *args, **kwargs):
        super(SparePartUserFilter, self).__init__(*args, **kwargs)
        self.filters['assigned_by'].field.label_from_instance = lambda obj: obj.get_full_name
        self.filters['engineer'].field.label_from_instance = lambda obj: obj.get_full_name
