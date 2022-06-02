import django_filters
from django.forms import DateInput
from django_filters import DateFilter, ModelChoiceFilter
from ticket.models.spare_part import SparePartUser
from ticket.models.ticket import Ticket, User


class TicketFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'По возрастанию'),
        ('descending', 'По убыванию')
    )

    start_date = DateFilter(field_name='received_at', lookup_expr='gte', label='С',
                            widget=DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'))
    end_date = DateFilter(field_name='received_at', lookup_expr='lte', label='По',
                          widget=DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'))
    ordering = django_filters.ChoiceFilter(label='Сортировать по', choices=CHOICES, method='sort_by_order')

    class Meta:
        model = Ticket
        fields = ['client', 'status']

    def sort_by_order(self, queryset, name, value):
        expression = 'received_at' if value == 'ascending' else '-received_at'
        return queryset.order_by(expression)


class SparePartUserFilter(django_filters.FilterSet):
    engineer = ModelChoiceFilter(queryset=User.objects.all(), label='Назначена кому')

    class Meta:
        model = SparePartUser
        fields = ['assigned_by', 'engineer', 'status']

    def __init__(self, *args, **kwargs):
        super(SparePartUserFilter, self).__init__(*args, **kwargs)
        self.filters['assigned_by'].field.label_from_instance = lambda obj: obj.get_full_name
        self.filters['engineer'].field.label_from_instance = lambda obj: obj.get_full_name

