from finance.views import *
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', accounts_view, name="accounts_view"),
    url(r'^account/(?P<pk>[0-9]+)/$', account_details, name='account_details'),
    url(r'^contacts/$', contacts_list, name='contacts'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^stats/$', stats_view, name='stats'),
    url(r'^profile/search_profile$', search_contact, name='search_contact'),
    url(r'^profile_form/(?P<id>\d+)/$', profile_form, name='profile_form'),
    url(r'^change_login_password/$', change_login_password, name='change_login_password'),
]