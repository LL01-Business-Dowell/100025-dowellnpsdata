from django.shortcuts import render
from django.urls import path, include
from .views import render_form, render_qrcode, render_iframe


urlpatterns = [
    path('', render_form, name='form'),
    path('qrcode', render_qrcode, name='qrcode'),
    path('iframe', render_iframe, name='iframe')
]