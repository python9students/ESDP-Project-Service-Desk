from django import forms
from django.contrib.auth import get_user_model
from ticket.models import Work, ProblemArea, ServiceObject, Client, Ticket
from django.core.exceptions import ValidationError
from django.forms import TextInput, widgets
from mptt.forms import TreeNodeMultipleChoiceField

User = get_user_model()


class ServiceObjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['active_from'] = self.instance.active_from.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.active_from else None

    class Meta:
        model = ServiceObject
        fields = '__all__'
        widgets = {
            'active_from': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                               attrs={'type': 'datetime-local'}),
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
    desired_to = forms.DateTimeField(required=False, label='Желаемая дата исполнения',
                                     widget=widgets.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                                  attrs={'type': 'datetime-local'}),
                                     )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['recieved_at'] = self.instance.recieved_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.recieved_at else None
            self.initial['desired_to'] = self.instance.desired_to.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.desired_to else None
            self.initial['closed_at'] = self.instance.closed_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.closed_at else None

    class Meta:
        model = Ticket
        widgets = {
            'recieved_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                               attrs={'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                             attrs={'type': 'datetime-local'}),
        }
        exclude = ("work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at", "cancel_reason",
                   "closed_at")


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
                                     widget=widgets.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                                  attrs={'type': 'datetime-local'}),
                                     )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['desired_to'] = self.instance.desired_to.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.desired_to else None
            self.initial['recieved_at'] = self.instance.recieved_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.recieved_at else None
            self.initial['closed_at'] = self.instance.closed_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.closed_at else None

    class Meta:
        model = Ticket
        widgets = {
            'recieved_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        exclude = ("driver", "executor", "work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at",
                   "cancel_reason", "status", "closed_at")


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
            'work_started_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                   attrs={'type': 'datetime-local'}),
            'work_finished_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                    attrs={'type': 'datetime-local'}),
            'ride_started_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                   attrs={'type': 'datetime-local'}),
            'ride_finished_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                    attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['client', 'service_object', 'priority', 'type', 'status', 'service_level', 'department', 'recieved_at',
                  'desired_to', 'operator', 'works', 'problem_areas', 'description', 'executor', 'driver', 'closed_at']
        for field in fields:
            self.fields[field].disabled = True
        if self.instance:
            self.initial['work_started_at'] = self.instance.work_started_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.work_started_at else None
            self.initial['work_finished_at'] = self.instance.work_finished_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.work_finished_at else None
            self.initial['ride_started_at'] = self.instance.ride_started_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.ride_started_at else None
            self.initial['ride_finished_at'] = self.instance.ride_finished_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.ride_finished_at else None

    def clean(self):
        cleaned_data = super().clean()
        work_started_at = cleaned_data['work_started_at']
        work_finished_at = cleaned_data['work_finished_at']
        ride_started_at = cleaned_data['ride_started_at']
        ride_finished_at = cleaned_data['ride_finished_at']
        if work_finished_at < work_started_at:
            self.add_error('work_started_at', ValidationError("Дата окончания работы не должны бать раньше начала"))

        if ride_finished_at < ride_started_at:
            self.add_error('ride_started_at',
                           ValidationError("Дата окончания поездки не должны бать раньше начала"))

        return cleaned_data


class TicketCancelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("cancel_reason",)
