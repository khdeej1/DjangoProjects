from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login




# Create your views here.

def index(request):
    name = request.GET.get("name") or "world!"
    return HttpResponse("Hello, "+name)


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('students.listStudents')  # For example, redirect to students listing or homepage.
    else:
        form = AuthenticationForm()
    return render(request, 'usermodule/login.html', {'form': form})

def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set and hash the password
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "You have successfully registered.")
            return redirect('users.login')  # redirect to login page after registration
    else:
        form = SignUpForm()
    return render(request, 'usermodule/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/users/login')