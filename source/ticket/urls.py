from django.urls import path, include

from ticket.views.ticket import (TicketCreateView,
                                 TicketListView,
                                 TicketDetailView,
                                 TicketUpdateView,
                                 TicketCancelView)
from ticket.views.clients import (ClientListView,
                                  ClientDetailView,
                                  ClientCreateView,
                                  ClientUpdateView,
                                  ClientDeleteView,
                                  IndexView)
from ticket.views.service_object import (ServiceObjectListView,
                                         ServiceObjectCreateView,
                                         ServiceObjectUpdateView,
                                         ServiceObjectDetailView,
                                         ServiceObjectDeleteView)

app_name = 'ticket'

service_object_urlpatterns = [
    path('', ServiceObjectListView.as_view(), name='service_object_list'),
    path('create/', ServiceObjectCreateView.as_view(), name='service_object_create'),
    path('update/<int:pk>/', ServiceObjectUpdateView.as_view(), name='service_object_update'),
    path('<int:pk>/', ServiceObjectDetailView.as_view(), name='service_object_detail'),
    path('delete/<int:pk>/', ServiceObjectDeleteView.as_view(), name='service_object_delete'),
]

client_urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]

ticket_urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path('<int:pk>/cancel/', TicketCancelView.as_view(), name='ticket_cancel'),
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('service_object/', include(service_object_urlpatterns)),
    path('client/', include(client_urlpatterns)),
    path('ticket/', include(ticket_urlpatterns)),
]
