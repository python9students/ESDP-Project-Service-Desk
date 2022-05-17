from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ticket.forms import User
from ticket.models import (CompanyType,
                           ServiceObjectType,
                           ServiceObjectModel,
                           Country,
                           Region,
                           City,
                           Client,
                           ServiceObject,
                           TicketType,
                           TicketStatus,
                           TicketPriority,
                           Work,
                           ProblemArea,
                           Department,
                           ServiceLevel,
                           Ticket,
                           CriterionType,
                           ContractStatus,
                           ContractType,
                           Contract)

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


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    search_fields = ("doc_number",)
    list_display = ("doc_number", "company_client", "valid_from", "valid_until", "status")


@admin.register(ServiceObject)
class ServiceObjectAdmin(admin.ModelAdmin):
    search_fields = ("serial_number",)
    list_display = ("serial_number", "client", "type", "is_installed", "address")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ("client",)
    list_display = ("__str__", "client", "service_object", "status", "received_at")


admin.site.unregister(User)


class CustomUserCreationForm(UserCreationForm):

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
        (_('Permissions'), {'fields': ('groups', ), }),
    )
