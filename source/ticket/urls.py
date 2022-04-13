from django.urls import path

from ticket.views.clients import IndexView
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

]
