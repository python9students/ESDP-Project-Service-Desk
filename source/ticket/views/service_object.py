from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from ticket.models import ServiceObject
from ticket.forms import ServiceObjectForm
from django.urls import reverse, reverse_lazy


class ServiceObjectListView(ListView):
    model = ServiceObject
    template_name = 'service_object/list.html'
    context_object_name = 'service_objects'


class ServiceObjectCreateView(CreateView):
    model = ServiceObject
    template_name = 'service_object/create.html'
    form_class = ServiceObjectForm

    def get_success_url(self):
        return reverse("ticket:service_object_detail", kwargs={"pk": self.object.pk})


class ServiceObjectUpdateView(UpdateView):
    model = ServiceObject
    template_name = 'service_object/update.html'
    context_object_name = 'service_object'
    form_class = ServiceObjectForm

    def get_success_url(self):
        return reverse("ticket:service_object_detail", kwargs={"pk": self.object.pk})


class ServiceObjectDetailView(DetailView):
    model = ServiceObject
    template_name = 'service_object/detail.html'
    context_object_name = 'service_object'


class ServiceObjectDeleteView(DeleteView):
    model = ServiceObject
    template_name = 'service_object/delete.html'
    context_object_name = 'service_object'
    success_url = reverse_lazy('ticket:service_object_list')
