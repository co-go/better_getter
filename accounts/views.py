# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from forms import CreateUserForm
from django.shortcuts import render

REDIRECT_FIELD_NAME = 'next'

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request, data=request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            auth_login(request, user)
            return HttpResponseRedirect('/')
    else:
        login_form = AuthenticationForm()
        signup_form = CreateUserForm(request)

        context = {
            'login_form': login_form,
            'signup_form': signup_form
        }

    return render(request, 'login.html', context)


def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect('/')
    else:
        login_form = AuthenticationForm(request)
        signup_form = CreateUserForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }

    return render(request, 'login.html', context)
