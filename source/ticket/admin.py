from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import admin
from ticket.forms import ContractAdminForm
from mptt.admin import MPTTModelAdmin
from datetime import date
from ticket.models import (CompanyType, ContractStatus, ContractType, ContractFiles,
                           Contract, ServiceObjectType, ServiceObjectModel, ServiceLevel,
                           CriterionType, ServiceObject, City, Country, Region, Department,
                           Client, SupplierCompany, SparePartUser, SparePart, Condition,
                           TicketPriority, TicketStatus, TicketType, Work, ProblemArea, Ticket, User)

admin.site.register(CompanyType)
admin.site.register(ServiceObjectType)
admin.site.register(ServiceObjectModel)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(TicketType)
admin.site.register(Work, MPTTModelAdmin)
admin.site.register(ProblemArea, MPTTModelAdmin)
admin.site.register(Department)
admin.site.register(ServiceLevel)
admin.site.register(CriterionType)
admin.site.register(ContractStatus)
admin.site.register(ContractType)
admin.site.register(Condition)
admin.site.register(SupplierCompany)
admin.site.register(SparePartUser)


class ContractFilesInline(admin.StackedInline):
    model = ContractFiles
    extra = 0


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "serial_number", "product_code", "quantity", "measure_unit", "condition")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    form = ContractAdminForm
    inlines = [ContractFilesInline]
    search_fields = ("doc_number",)
    list_display = ("doc_number", "company_client", "valid_from", "valid_until", "status")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_files(form.instance)


@admin.register(ServiceObject)
class ServiceObjectAdmin(admin.ModelAdmin):
    search_fields = ("serial_number",)
    list_display = ("serial_number", "client", "type", "is_installed", "address")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        service_object = get_object_or_404(ServiceObject, id=object_id)
        criterion = CriterionType.objects.get(name="Пост-гарантийный")
        if service_object.guarantee_valid_until:
            if service_object.guarantee_valid_until < date.today():
                service_object.criterion = criterion
                service_object.save()
                return super(ServiceObjectAdmin, self).change_view(request, object_id, form_url,
                                                                   extra_context=extra_context)
        return super(ServiceObjectAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ("client",)
    list_display = ("__str__", "client", "service_object", "status", "received_at")


admin.site.unregister(User)


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['groups'].required = True

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('groups',), }),
    )
