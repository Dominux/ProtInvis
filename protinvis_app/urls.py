from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('result/', result, name='result'),
]
