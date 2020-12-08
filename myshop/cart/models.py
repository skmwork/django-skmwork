from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from coupons.models import Coupon
from shop.models import Product
from decimal import Decimal


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

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Cart')
        verbose_name_plural = _('Cart')

    def __str__(self):
        return 'Cart {}'.format(self.id)

    def __len__(self):
        return self.active_items.count()

    @property
    def active_items(self):
        return self.items.filter(is_deleted=False)

    @property
    def total_price_after_discount(self):
        return self.total_price - self.total_discount

    @property
    def total_discount(self):
        return self.total_price * (self.discount / Decimal('100')) if self.coupon else 0

    @property
    def total_price(self):
        return sum(item.total_cost for item in self.active_items.all())

    @property
    def discount(self):
        return self.coupon.discount if self.coupon and self.coupon.is_valid else 0


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
