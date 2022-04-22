from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django.forms import widgets

from ticket.models import ServiceObject, Client, TicketPriority, TicketType, TicketStatus, ServiceLevel, Department, \
    Work

User = get_user_model()

class ServiceObjectForm(forms.ModelForm):
    class Meta:
        model = ServiceObject
        fields = '__all__'
        widgets = {
            'active_from': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                               attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class ClientForm(forms.ModelForm):
    website = forms.URLField(widget=TextInput)

    class Meta:
        model = Client
        fields = '__all__'


class ChiefForm(forms.Form):
    client = forms.MultipleChoiceField(queryset=Client.objects.all(), label="Клиент")
    service_object = forms.MultipleChoiceField(queryset=ServiceObject.objects.all(), label="Объект обслуживания")
    priority = forms.MultipleChoiceField(queryset=TicketPriority.objects.all(), label="Приоритет")
    type = forms.MultipleChoiceField(queryset=TicketType.objects.all(), label="Тип заявки")
    status = forms.MultipleChoiceField(queryset=TicketStatus.objects.all(), label="Статус заявки")
    service_level = forms.MultipleChoiceField(queryset=ServiceLevel.objects.all(), label="Уровень обслуживания")
    department = forms.MultipleChoiceField(queryset=Department.objects.all(), label="Департамент")
    created_at = forms.DateTimeField(label="Дата создания заявки")
    updated_at = forms.DateTimeField(label="Дата изменения заявки")
    recieved_at = forms.DateTimeField(label="Дата получения заявки")
    desired_to = forms.DateTimeField(label="Желаемая дата исполнения")
    operator = forms.MultipleChoiceField(queryset=User.objects.all(), label="Оператор")
    works = forms.MultipleChoiceField(queryset=Work.objects.all(), widget=widgets.CheckboxSelectMultiple)
    problem_areas = forms.MultipleChoiceField(queryset=Work.objects.all(), widget=widgets.CheckboxSelectMultiple)
    description = forms.CharField(max_length=1000, required=False, label="Описание",
                                  widget=widgets.Textarea(attrs={"rows": 5, "cols": 50}))
    executor = forms.MultipleChoiceField(queryset=User.objects.all(), label="Исполнитель")
    driver = forms.MultipleChoiceField(queryset=User.objects.all(), label="Водитель")
    cancel_reason = forms.CharField(max_length=225, required=True, label="Причина отмены заявки")