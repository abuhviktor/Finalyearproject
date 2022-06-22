from django.db import models

from apps.canteen.models import Canteen
from apps.product.models import Product
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    hostel_address = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    canteens = models.ManyToManyField(Canteen, related_name='orders')

    class Meta:
        ordering = ['-created_at']   #desending order

    def __str__(self):
        return self.first_name

# IntegerField, max length is ignored
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    canteen = models.ForeignKey(Canteen, related_name='items', on_delete=models.CASCADE)
    canteen_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "%s" % self.id

    def get_total_price(self):
        return self.price * self.quantity
