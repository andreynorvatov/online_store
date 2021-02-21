from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from .models import *
from .forms import OrderForm
from django.contrib import messages
from .utils import *

from django.core.mail import send_mail
from store_engine.settings import FROM_EMAIL

import random


def products_list(request):
    products = Product.objects.all()
    cart = Cart.objects.last()
    if not cart:
        cart = Cart.objects.create()
    return render(request, 'index.html', context={'products': products, 'cart': cart})


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.last()
        form = OrderForm(request.POST or None)

        return render(request, 'cart.html', context={'cart': cart, 'form': form})


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.last()
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart,
                                                                  product=product,
                                                                  final_price=product.price,
                                                                  product_id=product.id)
        print(f'Печать cart:{cart_product} {created}')
        if created:
            cart.products.add(cart_product)

        self.cart = cart
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.last()
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(cart=cart, product=product, product_id=product.id)
        cart.products.remove(cart_product)
        cart_product.delete()
        self.cart = cart
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.last()
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(cart=cart, product=product, product_id=product.id)
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        self.cart = cart
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, f'Количество изменено')
        return HttpResponseRedirect('/cart/')


class MakeOrderView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart.objects.last()
        self.cart = cart

        if form.is_valid():
            order_number = random.randint(100000, 999999)
            new_order = form.save(commit=False)
            new_order.name = form.cleaned_data['name']
            new_order.phone = form.cleaned_data['phone']
            new_order.email = form.cleaned_data['email']
            print(f'Печать form.cleaned_data:{form.cleaned_data}')
            new_order.save()
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()


            try:
                send_mail(
                    f'Тестовое здание, заказ № {order_number}',
                    f'{new_order.name}, заказ № {order_number} сформирован. В ближайшее время наш специалист '
                    f'свяжется с Вами по телефону {new_order.phone}.',
                    f'{FROM_EMAIL}',
                    [f'{new_order.email}'],
                    fail_silently=False
                )

                messages.add_message(
                    request,
                    messages.INFO,
                    f'Спасибо {new_order.name}, ваш заказ № {order_number} оформлен. В ближайшее '
                    f'время мы свяжемся с Вами по телефону {new_order.phone} для его подтверждения'
                )

            except Exception:
                messages.add_message(
                    request,
                    messages.INFO,
                    f'Спасибо {new_order.name}, ваш заказ № {order_number} оформлен, но почтовый клиент в данный момент не доступен.'
                )

            cart = Cart.objects.create()
            return HttpResponseRedirect('/cart/')
        print("Not Valid")
        messages.add_message(request, messages.INFO, f'Неверный Емэйл!')
        return HttpResponseRedirect('/cart/')
