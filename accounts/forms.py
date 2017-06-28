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
    class Meta:
        model = User
        fields = ('wf_email', 'wf_password')

    wf_email = forms.EmailField(label="Warframe Market Email", max_length=254)
    wf_password = forms.CharField(label="Warframe Market Password", widget=forms.PasswordInput)
