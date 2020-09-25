from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy


app_name = 'shop'
urlpatterns = [
    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    url(r'^$', views.product_list, name='product_list'),

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
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]