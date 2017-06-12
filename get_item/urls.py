from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/')),
    url(r'^(?P<item_name>.+)/$', views.get_item_details, name='get_item'),
]
