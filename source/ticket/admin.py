from django.contrib import admin

from ticket.models import (CompanyType,
                           ServiceObjectType,
                           ServiceObjectModel,
                           Country,
                           City,
                           Client,
                           ServiceObject,
                           TicketType,
                           TicketStatus,
                           TicketPriority,
                           Employee,
                           EmployeePosition)

admin.site.register(CompanyType)
admin.site.register(ServiceObjectType)
admin.site.register(ServiceObjectModel)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(ServiceObject)
admin.site.register(TicketPriority)
admin.site.register(TicketStatus)
admin.site.register(TicketType)
admin.site.register(Employee)
admin.site.register(EmployeePosition)
