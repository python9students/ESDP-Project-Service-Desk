import django_filters
from django.forms import DateInput
from django_filters import DateFilter

from ticket.models import Ticket


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
