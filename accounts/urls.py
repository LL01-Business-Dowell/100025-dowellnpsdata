from django.shortcuts import render
from django.urls import path, include
from .views import render_form, render_qrcode, render_iframe, get_event_id, text_qrcode_page


urlpatterns = [
    path('', render_form, name='form'),

    path('test',text_qrcode_page),

    path('get_eventid',get_event_id, name='get_event_id'),
    path('qrcode', render_qrcode, name='qrcode'),
    path('iframe', render_iframe, name='iframe')
]