from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from apps.product.models import Product
# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('frontpage')
    else:
        form = CreateUserForm

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)

                return redirect('logins')

        context = {
            'form': form
        }
        return render(request, 'core/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('frontpage')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('frontpage')
            else:
                messages.info(request, "username or password is incorrect")

        context = {}
        return render(request, 'core/login.html')

def logoutUser(request):
    logout(request)
    return redirect("logins")

@login_required(login_url='logins')
def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    return render(request, 'core/frontpage.html', {'newest_products': newest_products})

def contact(request):
    return render(request, 'core/contact.html')

# def navbar(request):
#     return render(request, 'core/navbar.html')

def userpage(request):
    newest_products = Product.objects.all()[0:8]
    return render(request, 'core/userPage.html', {'newest_products': newest_products})



