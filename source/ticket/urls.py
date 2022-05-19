from django.urls import path, include

from ticket.views.ticket import (TicketCreateView,
                                 TicketListView,
                                 TicketDetailView,
                                 TicketUpdateView,
                                 TicketCancelView,
                                 TicketCloseView,
                                 ChiefInfoDetailView, )
from ticket.views.ticket_api import TicketTimeView

app_name = 'ticket'

ticket_urlpatterns = [
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path('<int:pk>/cancel/', TicketCancelView.as_view(), name='ticket_cancel'),
    path('<int:pk>/close/', TicketCloseView.as_view(), name='ticket_close'),
    path('chief_info/', ChiefInfoDetailView.as_view(), name='chief_info'),
    path('<int:pk>/ticket_time/', TicketTimeView.as_view(), name='ticket_time_bar')
]

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
    path('ticket/', include(ticket_urlpatterns)),
]
