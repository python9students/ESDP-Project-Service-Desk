from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import ProtectedError
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ticket.models import Client
from ticket.forms import ClientForm
from django.urls import reverse, reverse_lazy


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

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, 'client/error.html', {'client': client})
