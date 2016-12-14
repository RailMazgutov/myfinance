from finance.views import *
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', accounts, name="accounts_view"),
    url(r'^account/(?P<pk>[0-9]+)/$', account_details, name='account_details'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile_form/(?P<id>\d+)/$', profile_form, name='profile_form'),
    url(r'^change_login_password/$', change_login_password, name='change_login_password'),
]