from finance.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', main, name="main"),
    url(r'charges/', charges, name="charges_view"),
]