from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django.forms import widgets
from mptt.forms import TreeNodeMultipleChoiceField

from ticket.models import ServiceObject, Client, Ticket, Work, ProblemArea

User = get_user_model()
from ticket.models import ServiceObject, Client, Ticket


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


class ChiefForm(forms.ModelForm):
    description = forms.CharField(required=False, max_length=1000,
                                  widget=widgets.Textarea(), label='Описание')
    cancel_reason = forms.CharField(required=False, max_length=255, label='Причина отмены заявки')
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')

    class Meta:
        model = Ticket
        fields = ("client", "service_object", "priority", "type",
                  "status", "service_level", "department", "recieved_at",
                  "desired_to", "operator", 'works',
                  "problem_areas", "description", "executor",
                  "driver", "closed_at", "cancel_reason")
        widgets = {
            'recieved_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                               attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'desired_to': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                              attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                             attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        exclude = ("work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at")


class EngineerForm(forms.ModelForm):
    client = forms.CharField(disabled=True)
    service_object = forms.CharField(disabled=True)
    priority = forms.CharField(disabled=True)
    type = forms.CharField(disabled=True)
    status = forms.CharField(disabled=True)
    service_level = forms.CharField(disabled=True)
    department = forms.CharField(disabled=True)
    created_at = forms.CharField(disabled=True)
    updated_at = forms.CharField(disabled=True)
    recieved_at = forms.CharField(disabled=True)
    desired_to = forms.CharField(disabled=True)
    operator = forms.CharField(disabled=True)
    works = forms.CharField(disabled=True)
    problem_areas = forms.CharField(disabled=True)
    description = forms.CharField(disabled=True)
    executor = forms.CharField(disabled=True)
    driver = forms.CharField(disabled=True)
    closed_at = forms.CharField(disabled=True)
    cancel_reason = forms.CharField(disabled=True)

    class Meta:
        model = Ticket
        fields = '__all__'

        widgets = {
            'work_started_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                                   attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'work_finished_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                                    attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ride_started_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                                   attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ride_finished_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                                    attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
