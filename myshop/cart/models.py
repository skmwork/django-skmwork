from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='carts', on_delete=models.CASCADE, null=True,
                             blank=True)
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_active = models.BooleanField(default=True)
    is_ordered = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon,
                               related_name='carts',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    discount = models.IntegerField(_('Discount'), default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')

    def __str__(self):
        return 'Cart {}'.format(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    is_active = models.BooleanField(default=True)
    is_ordered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def total_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
