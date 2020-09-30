"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = i18n_patterns(

    path('grappelli/', include('grappelli.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('admin/', admin.site.urls),
    url('login/', auth_views.LoginView.as_view(), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    url('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    url('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('', include('shop.urls')),   
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
