from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Canteen(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='canteen', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(canteen_paid=False, order__canteens__in=[self.id])
        return sum((items.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(canteen_paid=True, order__canteens__in=[self.id])
        return sum((items.product.price * item.quantity) for item in items)

