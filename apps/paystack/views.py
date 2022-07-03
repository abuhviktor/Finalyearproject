from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Payment
from . import forms

# Create your views here.
@login_required(login_url='logins')
def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'paystack/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm()
    return render(request, 'paystack/initiate_payment.html', {'payment_form': payment_form})    

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'verification Successful')
    else:
        messages.success(request, 'verification Failed.')
    return redirect('initiate_payment')

    