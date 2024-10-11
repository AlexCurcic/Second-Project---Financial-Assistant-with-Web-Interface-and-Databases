from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView, View, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import History
from .forms import CreateUserForm
import requests

def logout_view(request):
    logout(request)
    return redirect('login') 

def getBalance(user):
    transactions = History.objects.filter(user=user, status='success')

    total_deposits = sum(transaction.amount for transaction in transactions if transaction.type == 'deposit')
    total_withdrawals = sum(transaction.amount for transaction in transactions if transaction.type == 'withdraw')
    balance = total_deposits - total_withdrawals

    return float(balance)

def getCurrencyParams():
    response = requests.get('https://fake-api.apps.berlintech.ai/api/currency_exchange')
    
    if response.status_code == 200:
        data = response.json()
        currency_choices = [(currency, f'{currency} ({rate})') for currency, rate in data.items()]
        return [data, currency_choices]
    else:
        return [None, None]


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'app/create_account.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    success_url = reverse_lazy('main_menu')

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'app/main_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class BalanceOperationsView(LoginRequiredMixin, View):
    template_name = 'app/operations.html'
    
    def get(self, request):
        balance = getBalance(request.user)
        context = {
            'balance': balance,
            'username': request.user.username
        }
        return render(request, self.template_name, context)

    def post(self, request):
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = None
        operation_type = request.POST.get('operation')
        user = request.user

        if amount is None or operation_type not in ['deposit', 'withdraw']:
            balance = getBalance(user)
            context = {
                'balance': balance,
                'username': user.username
            }
            return render(request, self.template_name, context)

        if operation_type == 'withdraw':
            balance = getBalance(user)
            if balance < amount:
                status = 'failure'
            else:
                status = 'success'
        else:
            status = 'success'

        History.objects.create(
            user=user,
            amount=amount,
            type=operation_type,
            status=status
        )

        balance = getBalance(user)
        context = {
            'balance': balance,
            'username': user.username
        }
        return render(request, self.template_name, context)

class ViewTransactionHistoryView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'app/history.html'
    context_object_name = 'transactions'
    ordering = ['-datetime']

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

class CurrencyExchangeView(LoginRequiredMixin, View):
    template_name = 'app/currency_exchange.html'
    empty_context = {'currency_choices': [], 'amount': None, 'currency': None, 'exchanged_amount': None}

    def get(self, request):
        _, currency_choices = getCurrencyParams()
        context = {
            **self.empty_context,
            'currency_choices': currency_choices,
            'username': request.user.username
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data, currency_choices = getCurrencyParams()
        try:
            amount = float(request.POST.get('amount'))
        except (TypeError, ValueError):
            amount = None

        currency = request.POST.get('currency')

        if data is None or amount is None:
            return render(request, self.template_name, self.empty_context)

        exchange_rate = data.get(currency)
        exchanged_amount = round(amount * exchange_rate, 2) if exchange_rate else None

        context = {
            'currency_choices': currency_choices,
            'amount': amount,
            'currency': currency,
            'exchanged_amount': exchanged_amount,
            'username': request.user.username
        }
        return render(request, self.template_name, context)
