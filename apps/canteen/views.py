from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Canteen
from apps.product.models import Product

from .forms import ProductForm
# Create your views here.

def become_canteen(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            canteen = Canteen.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'canteen/become_canteen.html', {'form': form})

@login_required
def canteen_admin(request):
    canteen = request.user.canteen
    products = canteen.products.all()
    orders = canteen.orders.all()
    
    for order in orders:
        order.canteen_amount = 0
        order.canteen_paid_amount = 0
        order.fully_paid = True

        for item in canteen.items.all():
            if item.canteen == request.user.canteen:
                if item.canteen_paid:
                    order.canteen_paid_amount += item.get_total_price()
                else:
                    order.canteen_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'canteen/canteen_admin.html', {'canteen': canteen, 'products': products, 'orders': orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.canteen = request.user.canteen
            product.slug = slugify(product.title)
            product.save()

            return redirect('canteen_admin')
    else:
        form = ProductForm()

    return render(request, 'canteen/add_product.html', {'form': form})

@login_required
def edit_canteen(request):
    canteen = request.user.canteen

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            canteen. created_by.email = email
            canteen.created_by.save()

            canteen.name = name
            canteen.save()

            return redirect('canteen_admin')

    return render(request, 'canteen/edit_canteen.html', {'canteen': canteen})

def canteens(request):
    canteens = Canteen.objects.all()

    return render(request, 'canteen/canteens.html', {'canteens': canteens})

def canteen(request, canteen_id):
    canteen = get_object_or_404(Canteen, pk=canteen_id)

    return render(request, 'canteen/canteen.html', {'canteen': canteen})

