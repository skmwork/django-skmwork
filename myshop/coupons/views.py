from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from cart.session_cart import get_cart


@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        try:
            get_cart(request).set_coupon(form.cleaned_data['code'])
            messages.success(request, _('Coupon was applied successfully'))
        except Coupon.DoesNotExist:
            messages.error(request, _("Coupon wasn't found"))
    return redirect('cart:cart_detail')
