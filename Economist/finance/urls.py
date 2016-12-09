from finance.views import *
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', accounts, name="accounts_view"),
    url(r'^account/(?P<pk>[0-9]+)/$', account_details, name='account_details'),
]