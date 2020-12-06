from .models import Cart, CartItem
from decimal import Decimal
from coupons.models import Coupon
from django.utils import timezone



def get_cart(request):
    return SessionCart(request)


class SessionCart(object):
    def __init__(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session["session_key"] = 123
            request.session.cycle_key()
        session_key = request.session.session_key
        try:
            cart = Cart.objects.get(session_key=session_key, is_ordered=False)
        except Cart.DoesNotExist:
            cart = Cart(session_key=session_key)

        if request.user.id and not cart.user:
            cart.user = request.user

        self.cart = cart

    @property
    def active_items(self):
        return self.cart.items.filter(is_deleted=False).all()

    @property
    def total_price_after_discount(self):
        return self.total_cost - self.total_discount

    @property
    def total_discount(self):
        return self.total_cost * (self.cart.discount / Decimal('100'))

    @property
    def total_cost(self):
        return sum(item.total_cost for item in self.active_items.filter(is_deleted=False).all())

    def __len__(self):
        return self.cart.items.filter(is_deleted=False).count()

    def clear(self):
        self.cart.items.filter(is_deleted=True).update(is_deleted=True)

    def order(self):
        self.cart.items.update(is_ordered=True)
        self.cart.is_ordered = True
        self.cart.save()

    def remove(self, product):
        self.cart.items.filter(product_id=product.id, is_deleted=False).update(is_deleted=True)

    def set_coupon(self, code):
        if not self.cart.id:
            self.cart.save()
        now = timezone.now()
        coupon = Coupon.objects.get(code__iexact=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
        if coupon:
            self.cart.coupon = coupon
            self.cart.discount = coupon.discount
            self.cart.save()

    def add(self, product, quantity=1, update_quantity=False):
        if not self.cart.id:
            self.cart.save()
        try:
            cart_item = self.cart.items.get(product_id=product.id)
            if update_quantity or cart_item.is_deleted:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            if cart_item.is_deleted:
                cart_item.is_deleted = False
            cart_item.save()
        except CartItem.DoesNotExist:
            self.cart.items.create(product_id=product.id, quantity=quantity, cart=self, price=product.price)

