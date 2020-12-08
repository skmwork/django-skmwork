from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.session_cart import get_cart
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = cart
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart.active_items:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.price,
                                         quantity=item.quantity)
            cart.is_ordered = True
            cart.save()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
