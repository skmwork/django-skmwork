from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from cart.session_cart import SessionCart



@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        session_cart = SessionCart(request)
        coupon_is_applyed = session_cart.set_coupon(code)
        if coupon_is_applyed:
            messages.success(request, _('Coupon was applied successfully'))
        else:
            messages.error(request, _("Coupon wasn't found"))
    return redirect('cart:cart_detail')
