from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django.forms import widgets
from django.core.exceptions import ValidationError

from ticket.models import ServiceObject, Client, Ticket

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
                                  widget=widgets.Textarea())
    cancel_reason = forms.CharField(required=False, max_length=255)

    class Meta:
        model = Ticket
        fields = ("client", "service_object", "priority", "type",
                  "status", "service_level", "department", "recieved_at",
                  "desired_to", "operator", "works",
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
    class Meta:
        model = Ticket
        fields = '__all__'
