from django.urls import path
from .views import *

urlpatterns = [
    path('', MainMenuView.as_view(), name='main_menu'),
    path('auth/', CustomLoginView.as_view(), name='login'),
    path('create_account/', CreateUserView.as_view(), name='create_account'),
    path('logout/', logout_view, name='logout'),
    path('operations/', BalanceOperationsView.as_view(), name='operations'),
    path('currency_exchange/', CurrencyExchangeView.as_view(), name='currency_exchange'),
    path('history/', ViewTransactionHistoryView.as_view(), name='history'),
]
