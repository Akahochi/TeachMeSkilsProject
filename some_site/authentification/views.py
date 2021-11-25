from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as login_user,
    logout as logout_user
)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from authentification.forms import RegistrationForm, LoginForm
from authentification.bl import save_user

User = get_user_model()


def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('catalog:home'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # user = User(
            #     username=form.changed_data['username'],
            #     email=form.cleaned_data['email'],
            #     avatar=request.FILES.get('avatar')
            # )
            save_user(form)
            return redirect(reverse('catalog:home'))
    else:
        form = RegistrationForm()
    return render(
        request,
        'authentification/registration.html',
        {'form': form}
    )


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('catalog:home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                # username=form.cleaned_data['username'],  if use username and password
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                redirect_url = request.GET.get('next') or reverse('catalog:home')
                login_user(request, user)
                return redirect(redirect_url)
    else:
        form = LoginForm()
    next_url = request.GET.get('next', '')
    return render(
        request,
        'authentification/login.html',
        {'form': form, 'next': next_url}
    )


def logout(request):
    logout_user(request)
    return redirect(reverse('catalog:home'))