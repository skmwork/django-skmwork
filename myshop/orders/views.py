from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.session_cart import SessionCart
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    session_cart = SessionCart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = session_cart.cart
            if session_cart.coupon:
                order.coupon = session_cart.coupon
                order.discount = session_cart.coupon.discount
            order.save()
            for item in session_cart.active_items:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.price,
                                         quantity=item.quantity)
            # очистка корзины
            session_cart.order()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': session_cart, 'form': form})