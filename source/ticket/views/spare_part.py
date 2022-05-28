from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from ticket.filters import SparePartUserFilter
from ticket.forms import SparePartAssignForm, SparePartAssignFormSet
from ticket.models import SparePartUser, SparePart, Ticket


class SparePartAssignCreateView(LoginRequiredMixin, CreateView):
    model = SparePartUser
    template_name = 'spare_part/assign_create.html'
    form_class = SparePartAssignForm

    def get_success_url(self):
        return reverse("ticket:ticket_detail", kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        ticket = get_object_or_404(Ticket, pk=self.kwargs.get("pk"))
        context = super(SparePartAssignCreateView, self).get_context_data(**kwargs)
        context['formset'] = SparePartAssignFormSet(queryset=SparePartUser.objects.none())
        context['ticket'] = ticket
        return context

    def post(self, request, *args, **kwargs):
        formset = SparePartAssignFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return render(request, 'spare_part/assign_create.html', {'formset': formset})

    def form_valid(self, formset):
        ticket = get_object_or_404(Ticket, pk=self.kwargs.get("pk"))
        if not ticket.executor:
            messages.info(self.request, f'У этой заявки еще не назначен инженер, назначьте инженера и '
                                        f'возвращайтесь назначать запчасти')
            return redirect('ticket:ticket_detail', pk=self.kwargs.get("pk"))
        instances = formset.save(commit=False)
        for instance in instances:
            spare_part = SparePart.objects.get(id=instance.spare_part_id)
            if instance.quantity == 0:
                messages.warning(self.request, f'Вы не можете назначить запчастей в количестве: 0')
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset})
            elif spare_part.quantity > 0 and spare_part.quantity >= instance.quantity:
                instance.assigned_by = self.request.user
                instance.ticket = ticket
                instance.engineer = ticket.executor
                spare_part.quantity -= instance.quantity
                spare_part.save()
                instance.save()
                messages.success(self.request, f'Запчасти успешно назначены!')
                return redirect('ticket:ticket_detail', pk=self.kwargs.get("pk"))
            else:
                messages.error(self.request,
                               f'Количество запчасти {spare_part.name} на складе : {spare_part.quantity},'
                               f' а вы пытаетесь назначить : {instance.quantity}')
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset})
        messages.info(self.request, f'Запчасти назначены не были...')
        return super().form_valid(formset)


class SparePartUserListView(LoginRequiredMixin, ListView):
    model = SparePartUser
    template_name = 'spare_part/list.html'
    context_object_name = 'spare_parts'

    def get_queryset(self):
        spare_parts = super().get_queryset().order_by('-created_at')
        if self.request.user.has_perm('ticket.see_engineer_tickets') and not self.request.user.is_superuser:
            return spare_parts.filter(engineer=self.request.user)
        return spare_parts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['filter'] = SparePartUserFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SparePartReturnToWarehouse(View):
    def get(self, request, *args, **kwargs):
        spare_part = SparePartUser.objects.get(pk=kwargs.get('pk'))
        spare_part_warehouse = SparePart.objects.get(pk=spare_part.spare_part.pk)
        if spare_part.quantity == 1:
            spare_part.quantity = 0
            spare_part.status = 'Возвращенный'
            spare_part.save()
        else:
            spare_part.quantity -= 1
            spare_part.save()
        spare_part_warehouse.quantity += 1
        spare_part_warehouse.save()
        return redirect('ticket:spare_parts_list')
