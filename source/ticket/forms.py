from django import forms
from django.forms import TextInput
from django.forms import widgets
from mptt.forms import TreeNodeMultipleChoiceField

from ticket.models import ServiceObject, Client, Ticket, Work, ProblemArea


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
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')

    class Meta:
        model = Ticket
        widgets = {
            'recieved_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                               attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'desired_to': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                              attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                             attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        exclude = ("work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at", "cancel_reason")


class OperatorForm(forms.ModelForm):
    description = forms.CharField(required=False, max_length=1000,
                                  widget=widgets.Textarea(), label='Описание')
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')
    desired_to = forms.DateTimeField(required=False, label='Желаемая дата исполнения',
                                     widget=widgets.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                                                  attrs={'class': 'form-control',
                                                                         'type': 'datetime-local'}),
                                     )

    class Meta:
        model = Ticket
        widgets = {
            'recieved_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                               attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'),
                                             attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        exclude = ("driver", "executor", "work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at",
                   "cancel_reason")


class EngineerForm(forms.ModelForm):
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')

    class Meta:
        model = Ticket
        exclude = ("cancel_reason",)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['client', 'service_object', 'priority', 'type', 'status', 'service_level', 'department', 'recieved_at',
                  'desired_to', 'operator', 'works', 'problem_areas', 'description', 'executor', 'driver', 'closed_at']
        for field in fields:
            self.fields[field].disabled = True


class TicketCancelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("cancel_reason",)
