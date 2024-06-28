from django.urls import path
from pointBank.views import RegisterView, LoginView, TicketListView, BuyTicketView, UserTicketsView, CustomTokenRefreshView, send_code, check_code, autocomplete

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/tickets/', TicketListView.as_view(), name='tickets_list'),
    path('api/buy_ticket/', BuyTicketView.as_view(), name='buy_ticket'),
    path('api/user_tickets/', UserTicketsView.as_view(), name='user_tickets'),
    path('api/refresh_token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/autocomplete/', autocomplete, name='autocomplete'),
    path('api/send_code/', send_code, name='send_code'),
    path('api/check_code/', check_code, name='check_code'),
]
