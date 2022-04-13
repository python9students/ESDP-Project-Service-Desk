from django.urls import path

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

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('service_objects/', ServiceObjectListView.as_view(), name='service_object_list'),
    path('service_object/create/', ServiceObjectCreateView.as_view(), name='service_object_create'),
    path('service_object/update/<int:pk>/', ServiceObjectUpdateView.as_view(), name='service_object_update'),
    path('service_object/<int:pk>/', ServiceObjectDetailView.as_view(), name='service_object_detail'),
    path('service_object/delete/<int:pk>/', ServiceObjectDeleteView.as_view(), name='service_object_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
