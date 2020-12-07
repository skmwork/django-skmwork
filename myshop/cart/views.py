from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.session_cart import get_cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        get_cart(request).add(product=get_object_or_404(Product, id=product_id),
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    get_cart(request).remove(get_object_or_404(Product, id=product_id))
    return redirect('cart:cart_detail')


def cart_detail(request):
    return render(request,
                  'cart/detail.html',
                  {'cart': get_cart(request),
                   'coupon_apply_form': CouponApplyForm(),
                   })
