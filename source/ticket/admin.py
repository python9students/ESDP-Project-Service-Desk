from django.contrib import admin
from mptt.admin import MPTTModelAdmin

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
                           EmployeePosition,
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
admin.site.register(ServiceObject)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(TicketType)
admin.site.register(EmployeePosition)
admin.site.register(Work, MPTTModelAdmin)
admin.site.register(ProblemArea, MPTTModelAdmin)
admin.site.register(Department)
admin.site.register(ServiceLevel)
admin.site.register(Ticket)
admin.site.register(CriterionType)
admin.site.register(ContractStatus)
admin.site.register(ContractType)
admin.site.register(Contract)
