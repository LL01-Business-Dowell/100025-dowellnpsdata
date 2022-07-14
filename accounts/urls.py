from django.shortcuts import render
from django.urls import path, include
from accounts.views.helper import render_form, render_qrcode, render_iframe, get_event_id
from accounts import views

urlpatterns = [
    path('form/', render_form, name='form'),

    # path('test', text_qrcode_page),

    path('get_eventid', get_event_id, name='get_event_id'),
    path('qrcode', render_qrcode, name='qrcode'),
    path('iframe', render_iframe, name='iframe'),
    path('', views.DashboardView.as_view(), name='feedback'),
    path('set/survey/date/', views.SurveyDateView.as_view(), name='set_survey_date'),
]
