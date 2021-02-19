from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Цена')

    def __str__(self):
        return f'Продукт: {self.title}'


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', null=True, verbose_name='Корзина', on_delete=models.CASCADE,
                             related_name='related_products')
    product = models.ForeignKey(Product, null=True, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Общая Цена')

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Продукт: {self.product} (для корзины)'


class Cart(models.Model):
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')

    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=0, \
                                      verbose_name='Общая Цена')


def __str__(self):
    return f'Корзина: {self.id}'


class Order(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True,
                             blank=True)
    name = models.CharField(max_length=150, verbose_name='Имя', null=False, blank=False)
    phone = models.CharField(max_length=12, verbose_name='Телефон', null=False, blank=False)
    email = models.EmailField(max_length=254, verbose_name='Email', null=False, blank=False)

    def __str__(self):
        return str(self.id)
