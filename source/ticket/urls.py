from django.urls import path, include

from ticket.views.chief import ChiefTicketCreateView, ChiefTicketListView, ChiefTicketDetailView, ChiefTicketUpdateView
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
from ticket.views.engineer import EngineerTicketDetailView, EngineerTicketUpdateView, \
    EngineerTicketListView

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

chief_urlpatterns = [
    path('', ChiefTicketListView.as_view(), name='chief_ticket_list'),
    path('create/', ChiefTicketCreateView.as_view(), name='chief_ticket_create'),
    path('<int:pk>/', ChiefTicketDetailView.as_view(), name='chief_ticket_detail'),
    path('<int:pk>/update/', ChiefTicketUpdateView.as_view(), name='chief_ticket_update'),
]

engineer_urlpatterns = [
    path('<int:pk>/', EngineerTicketDetailView.as_view(), name='engineer_ticket_view'),
    path('<int:pk>/update/', EngineerTicketUpdateView.as_view(), name='engineer_update'),
    path('', EngineerTicketListView.as_view(), name="engineer_list")
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('service_object/', include(service_object_urlpatterns)),
    path('client/', include(client_urlpatterns)),
    path('chief/', include(chief_urlpatterns)),
    path('engineer/', include(engineer_urlpatterns))
]
