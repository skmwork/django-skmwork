from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, _('Coupon was applied successfully'))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, _("Coupon wasn't found"))
    return redirect('cart:cart_detail')
