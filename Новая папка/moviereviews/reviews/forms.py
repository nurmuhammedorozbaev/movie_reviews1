from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    nickname = forms.CharField(
        max_length=30,
        label='Никнейм',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ник',
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email',
        })
    )

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # username = nickname
        user.username = self.cleaned_data['nickname']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user