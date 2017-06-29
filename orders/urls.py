from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^place_order/$', views.place_order, name='place_order'),
    url(r'^(?P<username>.+)/$', views.get_user_orders, name='get_user_orders'),
    url(r'^$', views.get_orders, name='get_orders'),
]
