from django.contrib.auth import get_user_model
from ticket.models import ServiceObject, Client, Ticket, Work, ProblemArea
from django.forms import TextInput
from django.forms import widgets
from mptt.forms import TreeNodeMultipleChoiceField
from django import forms

User = get_user_model()


class ServiceObjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['active_from'] = self.instance.active_from.strftime('%Y-%m-%dT%H:%M') if self.instance.active_from else None

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
    cancel_reason = forms.CharField(required=False, max_length=255, label='Причина отмены заявки')
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['recieved_at'] = self.instance.recieved_at.strftime('%Y-%m-%dT%H:%M') if self.instance.recieved_at else None
            self.initial['desired_to'] = self.instance.desired_to.strftime('%Y-%m-%dT%H:%M') if self.instance.desired_to else None
            self.initial['closed_at'] = self.instance.closed_at.strftime('%Y-%m-%dT%H:%M') if self.instance.closed_at else None

    class Meta:
        model = Ticket
        fields = ("client", "service_object", "priority", "type",
                  "status", "service_level", "department", "recieved_at",
                  "desired_to", "operator", 'works',
                  "problem_areas", "description", "executor",
                  "driver", "closed_at", "cancel_reason")
        widgets = {
            'recieved_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                               attrs={'type': 'datetime-local'}),
            'desired_to': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                              attrs={'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                             attrs={'type': 'datetime-local'}),
        }
        exclude = ("work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at")


class OperatorForm(forms.ModelForm):
    description = forms.CharField(required=False, max_length=1000,
                                  widget=widgets.Textarea(), label='Описание')
    cancel_reason = forms.CharField(required=False, max_length=255, label='Причина отмены заявки')
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
            self.initial['desired_to'] = self.instance.desired_to.strftime('%Y-%m-%dT%H:%M') if self.instance.desired_to else None
            self.initial['recieved_at'] = self.instance.recieved_at.strftime('%Y-%m-%dT%H:%M') if self.instance.recieved_at else None
            self.initial['closed_at'] = self.instance.closed_at.strftime('%Y-%m-%dT%H:%M') if self.instance.closed_at else None

    class Meta:
        model = Ticket
        fields = ("client", "service_object", "priority", "type",
                  "status", "service_level", "department", "recieved_at",
                  "desired_to", "operator", "works", "problem_areas",
                  "description", "executor", "cancel_reason",)

        widgets = {
            'recieved_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'closed_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        exclude = ("driver", "executor", "work_started_at", "work_finished_at", "ride_started_at", "ride_finished_at",)


class EngineerForm(forms.ModelForm):
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 20}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(attrs={'size': 20}),
                                                label='Проблемные области')

    class Meta:
        model = Ticket
        fields = '__all__'

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
        self.fields['client'].disabled = True
        self.fields['service_object'].disabled = True
        self.fields['priority'].disabled = True
        self.fields['type'].disabled = True
        self.fields['status'].disabled = True
        self.fields['service_level'].disabled = True
        self.fields['department'].disabled = True
        self.fields['recieved_at'].disabled = True
        self.fields['desired_to'].disabled = True
        self.fields['operator'].disabled = True
        self.fields['works'].disabled = True
        self.fields['problem_areas'].disabled = True
        self.fields['description'].disabled = True
        self.fields['executor'].disabled = True
        self.fields['driver'].disabled = True
        self.fields['closed_at'].disabled = True
        self.fields['cancel_reason'].disabled = True
        if self.instance:
            self.initial['work_started_at'] = self.instance.work_started_at.strftime('%Y-%m-%dT%H:%M') if self.instance.work_started_at else None
            self.initial['work_finished_at'] = self.instance.work_finished_at.strftime('%Y-%m-%dT%H:%M') if self.instance.work_finished_at else None
            self.initial['ride_started_at'] = self.instance.ride_started_at.strftime('%Y-%m-%dT%H:%M') if self.instance.ride_started_at else None
            self.initial['ride_finished_at'] = self.instance.ride_finished_at.strftime('%Y-%m-%dT%H:%M') if self.instance.ride_finished_at else None
