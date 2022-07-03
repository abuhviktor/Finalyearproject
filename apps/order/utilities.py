# Separate the code from the views so their wouldn't be to much code
# importing from settings so later check on sendgrid and put it in the setting
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# send string as the email

from apps.cart.cart import Cart

from .models import Order, OrderItem


def checkout(request, first_name, last_name, hostel_address, phone, email, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, hostel_address=hostel_address, phone=phone, email=email, paid_amount=amount)
    
    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], canteen=item['product'].canteen, price=item['product'].price, quantity=item['quantity'])

        order.canteens.add(item['product'].canteen)

    return order


# def notify_canteen(order):
#     from_email = settings.DEFAULT_EMAIL_FROM

#     for canteen in order.canteens.all():
#         to_email = canteen.created_by.email
#         subject = 'New order'
#         text_content = 'You have a new order!'
#         html_content = render_to_string('order/email_notify_canteen.html', {'order': order, 'canteen': canteen})

#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()

# def notify_customer(order):
#     from_email = settings.DEFAULT_EMAIL_FROM

#     to_email = order.email
#     subject = 'Order confirmation'
#     text_content = 'Thank you for the order!'
#     html_content = render_to_string('order/email_notify_customer.html', {'order': order})

#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()




