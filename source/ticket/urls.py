from django.urls import path

from ticket.views.clients import IndexView

app_name = 'ticket'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]