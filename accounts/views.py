# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from forms import CreateUserForm, MarketForm
from django.shortcuts import render, redirect
import requests
from core import login, order

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


def settings(request):
    if request.method == "POST":
        market_form = MarketForm(request.POST)

        if market_form.is_valid():
            wf_email = market_form.cleaned_data.get('wf_email')
            wf_password = market_form.cleaned_data.get('wf_password')

            if (login.login(email=wf_email, password=wf_password) != None):
                print "Valid login"
                return redirect("settings")

            print "Invalid credentials"
        print "Enter in all fields"
    else:
        market_form = MarketForm()

    context = { "market_form": market_form }
    return render(request, 'settings.html', context)
