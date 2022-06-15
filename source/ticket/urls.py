from django.urls import path, include
from ticket.views import (TicketCreateView, TicketListView,
                          TicketDetailView, TicketUpdateView,
                          TicketCancelView, TicketCloseView,
                          ChiefInfoDetailView, SparePartUserListView,
                          SparePartAssignCreateView, TicketTimeView,
                          SparePartReturnToWarehouse, SparePartInstallation)
from ticket.views.ticket_api import ServiceObjectDetailView

app_name = 'ticket'

ticket_urlpatterns = [
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path('<int:pk>/cancel/', TicketCancelView.as_view(), name='ticket_cancel'),
    path('<int:pk>/close/', TicketCloseView.as_view(), name='ticket_close'),
    path('<int:pk>/ticket_time/', TicketTimeView.as_view(), name='ticket_time_bar'),
    path('chief_info/', ChiefInfoDetailView.as_view(), name='ticket_chief_info'),
]

spare_part_urlpatterns = [
    path('list/', SparePartUserListView.as_view(), name='spare_parts_list'),
    path('<int:pk>/assign-spare-part/', SparePartAssignCreateView.as_view(), name='spare_part_assign_create'),
    path('<int:pk>/return-spare-part/', SparePartReturnToWarehouse.as_view(), name='spare_part_return_warehouse'),
    path('<int:pk>/install-spare-part/', SparePartInstallation.as_view(), name='spare_part_install'),
]

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
    path('ticket/', include(ticket_urlpatterns)),
    path('spare-part/', include(spare_part_urlpatterns)),
    path('service_object/<int:pk>/detail/', ServiceObjectDetailView.as_view(), name='service_object_detail_view')
]
