from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(_('Coupon code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(_('Valid from'))
    valid_to = models.DateTimeField(_('Valid to'))
    discount = models.IntegerField(_('Discount'), validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(_('Active'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
