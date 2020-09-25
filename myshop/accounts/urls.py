from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse, reverse_lazy

app_name = 'accounts'

urlpatterns = [
    # previous login view
    # path('login/', views.user_login, name='login'),

    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
