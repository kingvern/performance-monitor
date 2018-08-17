"""per URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from per.mod import views, db



urlpatterns = [
    url(r'^hello$', views.helloo),
    url(r'^day$', db.day),
url(r'^index$', db.index),
url(r'^cycle$', db.cycle),
url(r'^demo', db.demo),
url(r'^test', db.test),
url(r'^add/$', db.add),
url(r'^locate/$', db.day_locate),
url(r'^detail/$', db.index_detail),
url(r'^check/$', db.cycle_check),
url(r'^ajax_list/$', db.ajax_list),
url(r'^ajax_dict/$', db.ajax_dict),
url(r'^ajax-detail/$', db.ajax_detail),
]
