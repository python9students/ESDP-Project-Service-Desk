from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from ticket.forms import SparePartAssignForm, SparePartAssignFormSet
from ticket.models import SparePartUser, SparePart


class SparePartAssignCreateView(CreateView):
    model = SparePartUser
    template_name = 'spare_part/assign_create.html'
    form_class = SparePartAssignForm

    def get_success_url(self):
        return reverse("ticket:chief_info")

    def get_context_data(self, **kwargs):
        context = super(SparePartAssignCreateView, self).get_context_data(**kwargs)
        context['formset'] = SparePartAssignFormSet(queryset=SparePartUser.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = SparePartAssignFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return render(request, 'spare_part/assign_create.html', {'formset': formset})

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            spare_part = SparePart.objects.get(id=instance.spare_part_id)
            if instance.quantity == 0:
                messages.warning(self.request, f'Вы не можете назначить запчастей в количестве: 0')
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset})
            elif spare_part.quantity > 0 and spare_part.quantity >= instance.quantity:
                instance.assigned_by = self.request.user
                spare_part.quantity -= instance.quantity
                spare_part.save()
                instance.save()
                messages.success(self.request, f'Запчасти успешно назначены!')
            else:
                messages.error(self.request, f'Количество запчасти {spare_part.name} на складе : {spare_part.quantity},'
                                             f' а вы пытаетесь назначить : {instance.quantity}')
                return render(self.request, 'spare_part/assign_create.html', {'formset': formset})
        return super().form_valid(formset)