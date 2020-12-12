from .models import OrderItem
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from cart.session_cart import get_cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@login_required
def order_create(request):
    cart = get_cart(request)
    if cart.is_empty:
        return redirect('cart:cart_detail')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = cart
            if cart.coupon and cart.coupon.is_valid:
                order.coupon = cart.coupon
                order.discount = cart.discount
            order.save()

            for item in cart.active_items:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.price,
                                         quantity=item.quantity)
            cart.is_ordered = True
            cart.save()

            messages.success(request, _("Your order has been successfully completed. Your order number is") + str(order.id))

            return redirect('shop:product_list')
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
