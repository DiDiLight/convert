from django.contrib import admin
from django.urls import path

from api.views import Converter

urlpatterns = [
    path(r'rates/', Converter.as_view(), name='rates'),
]
