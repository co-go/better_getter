from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', )


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )

class MarketForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
