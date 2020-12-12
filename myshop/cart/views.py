from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.session_cart import get_cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from .models import Cart, CartItem


@require_POST
def cart_add(request, product_id):
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

    quantity = cd['quantity']
    update_quantity = cd['update']
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    if not cart.id:
        cart.save()

    try:
        cart_item = cart.items.get(product_id=product)
    except CartItem.DoesNotExist:
        cart_item = None

    if cart_item is None:
        cart_item = CartItem(product_id=product.id, quantity=quantity, cart=cart, price=product.price)
    elif cart_item.is_deleted:
        cart_item.quantity = quantity
        cart_item.is_deleted = False
    elif update_quantity:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    get_cart(request).items.filter(product_id=get_object_or_404(Product, id=product_id).id, is_deleted=False) \
        .update(is_deleted=True)
    return redirect('cart:cart_detail')


def cart_detail(request):
    return render(request,
                  'cart/detail.html',
                  {'cart': get_cart(request),
                   'coupon_apply_form': CouponApplyForm(),
                   })
