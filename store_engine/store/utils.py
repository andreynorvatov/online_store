from django.db import models

def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data.get('final_price__sum')
    else:
        cart.final_price = 0
    cart.save()
