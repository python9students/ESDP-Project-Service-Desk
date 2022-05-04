from django.views.generic import ListView, DetailView
from ticket.models import ServiceObject


class ServiceObjectListView(ListView):
    model = ServiceObject
    template_name = 'service_object/list.html'
    context_object_name = 'service_objects'


class ServiceObjectDetailView(DetailView):
    model = ServiceObject
    template_name = 'service_object/detail.html'
    context_object_name = 'service_object'
