from django.contrib.auth.models import User
from django import forms
from .models import Profile
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторить пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth',)
        widgets = {'date_of_birth': DateInput()}
