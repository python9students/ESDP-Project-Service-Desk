from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy
from ticket.forms import ClientForm
from ticket.models import Client


# Create your views here.

class IndexView(TemplateView):
    template_name = 'base.html'


class ClientListView(ListView):
    model = Client
    template_name = 'client/list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'client/create.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse("ticket:client_detail", kwargs={"pk": self.object.pk})


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'client/update.html'
    context_object_name = 'client'
    form_class = ClientForm

    def get_success_url(self):
        return reverse("ticket:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('ticket:client_list')
