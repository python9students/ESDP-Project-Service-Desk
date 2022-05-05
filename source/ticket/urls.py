from django.urls import path, include

from ticket.views.ticket import (TicketCreateView,
                                 TicketListView,
                                 TicketDetailView,
                                 TicketUpdateView,
                                 TicketCancelView)
from ticket.views.service_object import (ServiceObjectListView,
                                         ServiceObjectDetailView)

app_name = 'ticket'

service_object_urlpatterns = [
    path('', ServiceObjectListView.as_view(), name='service_object_list'),
    path('<int:pk>/', ServiceObjectDetailView.as_view(), name='service_object_detail'),
]

ticket_urlpatterns = [
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path('<int:pk>/cancel/', TicketCancelView.as_view(), name='ticket_cancel'),
]

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
    path('service_object/', include(service_object_urlpatterns)),
    path('ticket/', include(ticket_urlpatterns)),
]
