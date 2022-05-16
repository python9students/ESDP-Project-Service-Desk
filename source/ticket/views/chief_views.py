from django.views.generic import ListView

from ticket.models import Ticket


class ChiefInfoDetailView(ListView):
    model = Ticket
    template_name = 'for_chief/chief_info_list_view.html'
    context_object_name = 'tickets'
    ordering = ["driver"]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     vasya = Ticket.objects.order_by('driver')
    #     context["vasya"] = vasya
    #     # context["choices"] = self.get_choices_with_answers_count(count, self.object.choices.all())
    #     return context

