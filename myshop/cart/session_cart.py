from .models import Cart, CartItem
from decimal import Decimal
from coupons.models import Coupon
from django.utils import timezone


def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()
    session_key = request.session.session_key

    try:
        cart = Cart.objects.filter(session_key=session_key, is_ordered=False).order_by('-updated')[0]
    except IndexError:
        cart = None

    if not cart and request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user, is_ordered=False).order_by('-updated')[0]
        except IndexError:
            cart = None

    if not cart:
        cart = Cart(session_key=session_key)

    if request.user.is_authenticated and not cart.user:
        cart.user = request.user

    return cart

