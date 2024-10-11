from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    '''
    Generate a form based on the User model with the fields:
    username, email, password1, password2
    '''