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
    pass # this line can be deleted 
    '''
    Write a function that finds the user's balance and returns it with the float data type. 
    To calculate the balance, calculate the sum of all user's deposits and the sum of all withdrawals.
    Then subtract the withdrawal amount from the deposit amount and return the result.
    '''
def getCurrencyParams():
    pass # this line can be deleted 
    '''
    Write a function that makes a GET request to the following address 
    https://fake-api.apps.berlintech.ai/api/currency_exchange

    if the response code is 200 return a list of two values:
    - a dictionary of data that came from the server
    - a list of strings based on the received data 
    mask to form the string f'{currency} ({rate})'.
    example string: 'USD (1.15)'

    if the server response code is not 200 you should 
    return the list [None, None]
    '''


class CreateUserView(CreateView):
    '''
    Finalize this class. It should create a new user.
    The model should be the User model
    The CreateUserForm model should be used as a form.
    The file create_account.html should be used as a template.
    If the account is successfully created, it should redirect to the page with the name login
    '''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''
        return context

class CustomLoginView(LoginView):
    '''
    Modify this class. 
    specify the login.html file as the template
    if authentication is positive, add redirect to main_menu page
    '''

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''
        return context

class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'app/main_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''
        return context

class BalanceOperationsView(LoginRequiredMixin, View):
    template_name = 'app/operations.html'
    
    def get(self, request):
        pass # this line can be deleted 
        '''
        This method should return the page given in template_name with a context.

        Context is a dictionary with balance and username keys.
        The balance key contains the result of the getBalance function
        username contains the username of the user.
        '''

    def post(self, request):
        pass # this line can be deleted 
        '''
        This method should process a balance transaction.
        For this purpose it is necessary to add an entry to the History model. 
        
        status - if the amount on the account is not enough when attempting to withdraw funds, the status is failure, otherwise withdraw
        amount - amount of operation, obtained from the form
        type - type of operation (withdraw/deposit), the value is obtained from the form.
        user - object of the current user

        This method should return the page given in template_name with a context.

        Context is a dictionary with balance and username keys.
        The balance key contains the result of the getBalance function (after account update)
        username contains the username of the user.
        '''

class ViewTransactionHistoryView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'app/history.html'
    context_object_name = 'transactions'
    ordering = ['-datetime']

    def get_queryset(self):
        '''
        This method should return the entire transaction history of the current user
        '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        Add the 'username' key with the value of username to the context.
        '''
        return context

class CurrencyExchangeView(LoginRequiredMixin, View):
    template_name = 'app/currency_exchange.html'
    empty_context = {'currency_choices': [], 'amount': None, 'currency': None, 'exchanged_amount': None}

    def get(self, request):
        _, currency_choices = getCurrencyParams()
        '''
        Generate a context variable with all values from empty_context and the converted values of currency_choices and username
        currency_choices contains the value of the currency_choices variable
        username contains the name of the current user
        '''
        return render(request, self.template_name, context)

    def post(self, request):
        data, currency_choices = getCurrencyParams()
        '''
            Improve this method:
            1) add the process of forming the variable amount.
            If the amount value from the form is converted to float type, then write the amount value from the form converted to float to the amount variable. Otherwise, write None.
            2) add a currency variable that contains the currency value from the form.
            3) if the variables data or amount contain None, return page with empty context (empty_context). Otherwise, perform the following steps
            4) generate the exchange_rate variable by calculating the corresponding value from the data variable
            5) generate the exchanged_amount variable, which contains the converted currency to two decimal places.
            6) form a context from the previously created variables and return a template with it.
        '''
