from django.urls import path
from .views import *

urlpatterns = [
    path('', products_list, name='products_list_url'),
    path('cart/', CartView.as_view(), name='cart_url'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]
