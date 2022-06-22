from django import forms

# for validation
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()
