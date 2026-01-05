from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    nickname = forms.CharField(
        label='Никнейм',
        max_length=30,
        required=True
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password1', 'password2')