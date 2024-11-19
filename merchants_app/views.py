from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')
    # return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')
