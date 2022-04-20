from django.shortcuts import render
from django.urls import path, include
from .views import render_form, render_qrcode


urlpatterns = [
    path('', render_form, name='form'),
    path('qrcode', render_qrcode)
]