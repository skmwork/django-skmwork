from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse, reverse_lazy

app_name = 'accounts'

urlpatterns = [
    # previous login view
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/registration/login.html'),
         {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/registration/logged_out.html'),
         name='logout'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/registration/password_change_form.html',
                                                                   success_url = reverse_lazy('accounts:password_change_done')),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/registration/password_change_done.html'),
         name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html',
                                                                 success_url = reverse_lazy('accounts:password_reset_done')),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
