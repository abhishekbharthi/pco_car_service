from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .decorators import mechanic_required
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            role = user.userprofile.role

            if role == 'MECHANIC':
                return redirect('mechanic_dashboard')

            # Admin & Super Admin go to Django admin
            if role in ['ADMIN', 'SUPER_ADMIN']:
                return redirect('/admin/')

        return render(request, 'auth/login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/accounts/login/')
@mechanic_required
def mechanic_dashboard(request):
    return render(request, 'dashboard/mechanic_dashboard.html')
