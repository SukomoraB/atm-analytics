# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import View

from atm_analytics.authentication.forms import CustomAuthenticationForm


class Login(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, 'authentication/login.html', {
            'form': form
        })

    @staticmethod
    def post(request, *args, **kwargs):
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, _("User or incorrect password"))
                return render(request, 'authentication/login.html', {
                    'form': form
                })
            if not user.is_active:
                messages.info(request, _("Inactive user"))
                return render(request, 'authentication/login.html', {
                    'form': form
                })

            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            login(request, user)
            return redirect('base:dashboard')

        return render(request, 'authentication/login.html', {
            'form': form
        })
