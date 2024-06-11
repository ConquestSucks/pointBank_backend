from django.urls import path
from pointBank.views import RegisterView, LoginView, TicketListView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/tickets/', TicketListView.as_view(), name='tickets_list')
]
