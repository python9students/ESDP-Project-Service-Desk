from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from ticket.filters import SparePartUserFilter
from ticket.forms import SparePartAssignForm, SparePartAssignFormSet, SparePartInstall
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
        context['formset'] = SparePartAssignFormSet(
            queryset=SparePartUser.objects.filter(ticket_id=ticket.id, engineer_id=ticket.executor))
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
            messages.error(self.request, f'У этой заявки еще не назначен инженер, назначьте инженера и '
                                         f'возвращайтесь назначать запчасти')
            return redirect('ticket:ticket_detail', pk=self.kwargs.get("pk"))
        instances = formset.save(commit=False)
        for instance in instances:
            spare_part = SparePart.objects.get(id=instance.spare_part_id)
            if instance.quantity == 0:
                messages.error(self.request, f'Вы не можете назначить запчастей в количестве: 0')
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset, 'ticket': ticket})
            elif spare_part.quantity > 0 and spare_part.quantity >= instance.quantity:
                for s in SparePartUser.objects.all():
                    if s.spare_part_id == instance.spare_part_id and s.ticket_id == ticket.id:
                        messages.error(self.request, f'Назначать запчасти с одинаковыми серийными номерами нельзя!')
                        return render(self.request, 'spare_part/assign_create.html',
                                      {'formset': formset, 'ticket': ticket})
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
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset, 'ticket': ticket})
        messages.warning(self.request, f'Запчасти назначены не были...')
        return super().form_valid(formset)


class SparePartUserListView(LoginRequiredMixin, ListView):
    model = SparePartUser
    template_name = 'spare_part/list.html'
    context_object_name = 'spare_parts'
    paginate_by = 6
    paginate_orphans = 0

    def get_queryset(self):
        spare_parts = super().get_queryset().order_by('-created_at')
        query = Q(status="assigned") | Q(status="set")
        if self.request.user.has_perm('ticket.see_engineer_tickets') and \
                self.request.user.has_perm('ticket.see_engineer_spare_parts') \
                and not self.request.user.is_superuser:
            return spare_parts.filter(engineer=self.request.user).filter(query)
        return SparePartUserFilter(self.request.GET, queryset=spare_parts).qs

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
            spare_part.status = 'returned'
            spare_part.save()
            messages.success(self.request, f'Запчасть {spare_part_warehouse} успешно возвращена на склад!')
        elif spare_part.status == 'returned':
            messages.error(self.request, f'Невозможно вернуть на склад, так как эта запчасть уже возвращена!')
        elif spare_part.status == 'set':
            messages.error(self.request, f'Невозможно вернуть на склад, так как эта запчасть уже установлена!')
        else:
            spare_part.quantity -= 1
            spare_part.save()
            messages.success(self.request,
                             f'Запчасть {spare_part_warehouse} в количестве: *1* успешно возвращена на склад!')
        spare_part_warehouse.quantity += 1
        spare_part_warehouse.save()
        return redirect('ticket:spare_parts_list')


class SparePartInstallation(View):
    def get(self, request, *args, **kwargs):
        spare_part = SparePartUser.objects.get(pk=kwargs.get('pk'))
        ticket = Ticket.objects.get(pk=spare_part.ticket_id)
        if (spare_part.status == 'assigned' or spare_part.status == 'set') and spare_part.quantity == 1:
            spare_part.status = 'set'
            spare_part.service_object = ticket.service_object
            spare_part.quantity -= 1
            spare_part.save()
            messages.success(self.request,
                             f'Запчасть {spare_part.spare_part} успешно установлена '
                             f'на объект {spare_part.service_object}!')
        elif (spare_part.status == 'assigned' or spare_part.status == 'set') and spare_part.quantity > 1:
            spare_part.quantity -= 1
            spare_part.service_object = ticket.service_object
            spare_part.save()
            messages.success(self.request, f'Запчасть {spare_part.spare_part} в количестве *1*'
                                           f'успешно установлена на объект {spare_part.service_object}!')
        if spare_part.status == 'set':
            messages.error(self.request, f'Невозможно установить, так как эта запчасть уже установлена!')
        if spare_part.status == 'returned':
            messages.error(self.request, f'Невозможно установить, так как эта запчасть уже возвращена!')
        return redirect('ticket:spare_parts_list')
