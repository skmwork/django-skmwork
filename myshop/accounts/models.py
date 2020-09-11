from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(_('Birth date'), blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
