# import stripe pip install stripe
import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_canteen, notify_customer
# Create your views here.

def cart_detail(request):
    cart = Cart(request)

    # IF FORM HAS BEEN SUBMITTED
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # initialize the stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            charge = stripe.Charge.create(
                amount=int(cart.get_total_cost() * 100),
                currency='NGN',
                description='Charge for the canteen',
                source=stripe_token
            )

            first_name = form.cleaned_data['First Name']
            last_name = form.cleaned_data['Last Name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            hostel_address = form.cleaned_data['hostel_address']
            order = checkout(request, first_name, last_name, phone, email, hostel_address, cart.get_total_cost())

            cart.clear()

            notify_customer(order)
            notify_canteen(order)

            return redirect('success')
        else:
            form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')
    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})
    # stripe_pub_key
    # ': settings.STRIPE_PUB_KEY}

def success(request):
    return render(request, 'cart/success.html')


