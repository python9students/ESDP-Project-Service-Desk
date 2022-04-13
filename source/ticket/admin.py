from django.contrib import admin

from ticket.models import (CompanyType,
                           ServiceObjectType,
                           ServiceObjectModel,
                           Country,
                           City,
                           Client,
                           ServiceObject)

admin.site.register(CompanyType)
admin.site.register(ServiceObjectType)
admin.site.register(ServiceObjectModel)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(ServiceObject)
