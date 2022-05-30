from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ticket.models import Work, ProblemArea, Ticket, ContractFiles, Contract, SparePartUser, Client, ServiceObject, \
    TicketPriority, TicketType, ServiceLevel, Department
from django.forms import widgets, BaseModelForm, modelformset_factory
from django.utils import timezone
from mptt.forms import TreeNodeMultipleChoiceField
from django import forms

User = get_user_model()


class TicketFormValidationMixin(BaseModelForm):
    def clean(self):
        cleaned_data = super().clean()
        received_at = cleaned_data['received_at']
        desired_to = cleaned_data['desired_to']
        work_started_at = cleaned_data['work_started_at']
        work_finished_at = cleaned_data['work_finished_at']
        ride_started_at = cleaned_data['ride_started_at']
        ride_finished_at = cleaned_data['ride_finished_at']

        if received_at and received_at > timezone.now():
            self.add_error('received_at',
                           ValidationError("Дата получения заявки не может быть позже чем время сейчас"))
            self.fields['received_at'].widget.attrs.update({'style': 'border-color:red;'})
        if received_at and desired_to:
            if received_at > desired_to:
                self.add_error('desired_to',
                               ValidationError(
                                   "Желаемая дата исполнения не может быть позже чем дата получения заявки"))
                self.fields['desired_to'].widget.attrs.update({'style': 'border-color:red;'})

        if ride_finished_at and ride_started_at:
            if ride_finished_at < ride_started_at:
                self.add_error('ride_finished_at',
                               ValidationError("Дата окончания поездки не может быть раньше начала поездки"))
                self.fields['ride_finished_at'].widget.attrs.update({'style': 'border-color:red;'})
        if ride_started_at and work_started_at:
            if work_started_at < ride_started_at:
                self.add_error('work_started_at',
                               ValidationError("Дата начала работ не может быть раньше начала поездки"))
                self.fields['work_started_at'].widget.attrs.update({'style': 'border-color:red;'})
        if ride_started_at and work_finished_at:
            if work_finished_at < ride_started_at:
                self.add_error('work_finished_at',
                               ValidationError("Дата окончания работ не может быть раньше начала поездки"))
                self.fields['work_finished_at'].widget.attrs.update({'style': 'border-color:red;'})
        if work_finished_at and work_started_at:
            if work_finished_at < work_started_at:
                self.add_error('work_finished_at',
                               ValidationError("Дата окончания работ не может быть раньше начала работ"))
                self.fields['work_finished_at'].widget.attrs.update({'style': 'border-color:red;'})
        if ride_finished_at and work_finished_at:
            if ride_finished_at < work_finished_at:
                self.add_error('ride_finished_at',
                               ValidationError("Дата окончания поездки не может быть раньше окончания работ"))
                self.fields['ride_finished_at'].widget.attrs.update({'style': 'border-color:red;'})
        if ride_finished_at and work_started_at:
            if ride_finished_at < work_started_at:
                self.add_error('ride_finished_at',
                               ValidationError("Дата окончания поездки не может быть раньше начала работ"))
                self.fields['ride_finished_at'].widget.attrs.update({'style': 'border-color:red;'})
        return cleaned_data


class ChiefForm(forms.ModelForm, TicketFormValidationMixin):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Клиент',
                                    widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    service_object = forms.ModelChoiceField(queryset=ServiceObject.objects.all(), label='Объект обслуживания',
                                            widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    priority = forms.ModelChoiceField(queryset=TicketPriority.objects.all(), label='Приоритет',
                                      widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    type = forms.ModelChoiceField(queryset=TicketType.objects.all(), label='Тип заявки',
                                  widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    service_level = forms.ModelChoiceField(queryset=ServiceLevel.objects.all(), label='Уровень обслуживания',
                                           widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label='Департамент',
                                        widget=widgets.Select(attrs={'class': 'form-select form-select-sm'}))
    received_at = forms.DateTimeField(label='Дата получения заявки',
                                      widget=widgets.DateTimeInput(
                                          format='%d/%m/%Y %H:%M',
                                          attrs={'type': 'datetime-local',
                                                 'class': 'form-control form-control-sm'}),
                                      )
    description = forms.CharField(required=False, max_length=1000,
                                  widget=widgets.Textarea(attrs={'class': 'form-control', 'cols': 65, 'rows': 4}),
                                  label='Описание')
    work_done = forms.CharField(required=False, max_length=1000,
                                widget=widgets.Textarea(attrs={'class': 'form-control', 'cols': 65, 'rows': 4}),
                                label='Проделанная работа')
    executor = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Исполнитель',
                                      widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    driver = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Водитель',
                                    widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    works = TreeNodeMultipleChoiceField(queryset=Work.objects.all(),
                                        widget=widgets.SelectMultiple(attrs={'size': 6.5, 'class': 'form-select'}),
                                        label='Работы')
    problem_areas = TreeNodeMultipleChoiceField(queryset=ProblemArea.objects.all(),
                                                widget=widgets.SelectMultiple(
                                                    attrs={'size': 6.5, 'class': 'form-select'}),
                                                label='Проблемные области')
    desired_to = forms.DateTimeField(required=False, label='Желаемая дата и время исполнения',
                                     widget=widgets.DateTimeInput(
                                         format='%d/%m/%Y %H:%M',
                                         attrs={'type': 'datetime-local',
                                                'class': 'form-control form-control-sm'}),
                                     )
    work_started_at = forms.DateTimeField(required=False, label='Дата начала работ',
                                          widget=widgets.DateTimeInput(
                                              format='%d/%m/%Y %H:%M',
                                              attrs={'type': 'datetime-local',
                                                     'class': 'form-control form-control-sm'}),
                                          )
    work_finished_at = forms.DateTimeField(required=False, label='Дата окончания работ',
                                           widget=widgets.DateTimeInput(
                                               format='%d/%m/%Y %H:%M',
                                               attrs={'type': 'datetime-local',
                                                      'class': 'form-control form-control-sm'}),
                                           )
    ride_finished_at = forms.DateTimeField(required=False, label='Дата окончания поездки',
                                           widget=widgets.DateTimeInput(
                                               format='%d/%m/%Y %H:%M',
                                               attrs={'type': 'datetime-local',
                                                      'class': 'form-control form-control-sm'}),
                                           )
    ride_started_at = forms.DateTimeField(required=False, label='Дата начала поездки',
                                          widget=widgets.DateTimeInput(
                                              format='%d/%m/%Y %H:%M',
                                              attrs={'type': 'datetime-local',
                                                     'class': 'form-control form-control-sm'}),
                                          )
    expected_finish_date = forms.DateTimeField(required=False, label='Ожидаемая дата завершения',
                                               widget=widgets.DateTimeInput(
                                                   format='%d/%m/%Y %H:%M',
                                                   attrs={'type': 'datetime-local',
                                                          'class': 'form-control form-control-sm'}),
                                               )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['received_at'] = self.instance.received_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.received_at else None
            self.initial['desired_to'] = self.instance.desired_to.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.desired_to else None
            self.initial['closed_at'] = self.instance.closed_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.closed_at else None
            self.initial['work_started_at'] = self.instance.work_started_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.work_started_at else None
            self.initial['work_finished_at'] = self.instance.work_finished_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.work_finished_at else None
            self.initial['ride_started_at'] = self.instance.ride_started_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.ride_started_at else None
            self.initial['ride_finished_at'] = self.instance.ride_finished_at.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.ride_finished_at else None
            self.initial['expected_finish_date'] = self.instance.expected_finish_date.strftime(
                '%Y-%m-%dT%H:%M') if self.instance.expected_finish_date else None
        self.fields['executor'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
        self.fields['driver'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

    class Meta:
        model = Ticket
        exclude = ("cancel_reason", "closed_at", "operator", "status", "close_commentary",)


class EngineerForm(ChiefForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['client', 'service_object', 'priority', 'type', 'status', 'service_level', 'department',
                  'received_at', 'desired_to', 'operator', 'description', 'executor', 'driver', 'expected_finish_date']
        for field in fields:
            self.fields[field].disabled = True

    class Meta:
        model = Ticket
        exclude = ("cancel_reason", "close_commentary", "closed_at")


class TicketCancelForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("cancel_reason",)


class TicketCloseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("close_commentary",)


# Форма для добавления нескольких файлов в контракт
class ContractAdminForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"

    current_document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Действующий документ"),
        required=False,
    )

    def save_files(self, contract):
        for upload in self.files.getlist("current_document"):
            file = ContractFiles(contract=contract, current_document=upload)
            file.save()


class SparePartAssignForm(forms.ModelForm):
    class Meta:
        model = SparePartUser
        exclude = ['created_at', 'assigned_by', 'engineer']


SparePartAssignFormSet = modelformset_factory(SparePartUser, form=SparePartAssignForm,
                                              fields=['spare_part', 'quantity'], extra=6)


class SparePartUserListForm(forms.ModelForm):
    class Meta:
        model = SparePartUser
        fields = "__all__"


class SparePartInstall(forms.ModelForm):
    class Meta:
        model = SparePartUser
        fields = ['service_object']
        exclude = ['spare_part', 'engineer', 'quantity', 'created_at', 'assigned_by', 'ticket', 'status']
