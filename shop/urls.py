from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy


app_name = 'shop'
urlpatterns = [
    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]