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

    def __len__(self):
        return self.items.filter(is_deleted=False).count()

    @property
    def total_cost(self):
        return sum(item.total_cost for item in self.items.all())

    @property
    def active_items(self):
        return self.items.filter(is_deleted=False).all()

    @property
    def total_price_after_discount(self):
        return self.total_cost - self.total_discount

    @property
    def total_discount(self):
        return self.total_cost * (self.discount / Decimal('100')) 

    def clear(self):
        self.cart.items.update(is_deleted=True)

    def order(self):
        self.items.update(is_ordered=True)
        self.is_ordered = True
        self.save()

    def remove(self, product):
        self.cart.items.filter(product_id=product.id, is_deleted=False).update(is_deleted=True)

    def set_coupon(self, code):
        try:
            now = timezone.now()
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            if coupon:
                self.coupon = coupon
                self.discount = coupon.discount
                self.save()
            return True
        except Coupon.DoesNotExist:
            return False

    def add(self, product, quantity=1, update_quantity=False):
        try:
            cart_item = self.items.get(product_id=product.id)
            if update_quantity or cart_item.is_deleted:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            if cart_item.is_deleted:
                cart_item.is_deleted = False
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem(product_id=product.id, quantity=quantity, cart=self, price=product.price)
            cart_item.save()


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
