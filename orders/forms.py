from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'postal_code', 'city']
        error_messages = {
            'first_name': {
                # for example:
                'required': "This writer's name is too long.",
            },
        }