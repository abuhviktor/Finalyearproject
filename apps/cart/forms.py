from django import forms

# the phone variable check it
class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    hostel_address = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=200)
    stripe_token = forms.CharField(max_length=200)



