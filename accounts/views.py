# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from forms import CreateUserForm, MarketForm
from django.shortcuts import render, redirect
import requests
from core import login as wf_login

def signup(request):
    if request.method == "POST":
        signup_form = CreateUserForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            auth_login(request, user)
            return redirect('/')
    else:
        signup_form = CreateUserForm()

    login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }

    return render(request, 'login.html', context)


def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('/')
    else:
        login_form = AuthenticationForm(request)

    signup_form = CreateUserForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }

    return render(request, 'login.html', context)

@login_required
def settings(request):
    err = None
    valid = None
    user = request.user

    if request.method == "POST":
        market_form = MarketForm(request.POST)

        if market_form.is_valid():
            wf_email = market_form.cleaned_data.get('wf_email')
            wf_password = market_form.cleaned_data.get('wf_password')

            if (wf_login.login_user(email=wf_email, password=wf_password) != None):
                print "[LOGIN] Valid!"
                user.wf_email = wf_email
                user.wf_password = wf_password
                user.save()
            else:
                err = "Invalid credentials"
        else:
            err = "Enter in all fields"
    else:
        market_form = MarketForm(initial={'wf_email': user.wf_email, 'wf_password': "loluthot"})

    if (user.wf_email != "" and user.wf_password != ""):
        valid = True

    context = { "market_form": market_form,
                "err": err,
                "valid": valid }

    return render(request, 'settings.html', context)
