from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Coupon'),
                                                                      'class': 'textinput textInput form-control'}))

