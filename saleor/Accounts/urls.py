from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from saleor.Accounts.views import login, register


urlpatterns = [                     
    url(r'^$', login),
    url(r'^login', login),
    url(r'^register', register),
]