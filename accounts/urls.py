from django.shortcuts import render
from django.urls import path, include
from accounts.views.helper import render_form, render_qrcode, render_iframe, get_event_id
from accounts import views

urlpatterns = [
    path('login/', views.LoInFunc.as_view(), name='login'),
    path('form/', render_form, name='form'),

    # path('test', text_qrcode_page),

    path('get_eventid', get_event_id, name='get_event_id'),
    path('qrcode', render_qrcode, name='qrcode'),
    path('iframe', render_iframe, name='iframe'),
    path('', views.DashboardView.as_view(), name='feedback'),
    path('<int:pk>/set/survey/date/', views.SurveyDateView.as_view(), name='set_survey_date'),
    path('<int:pk>/create/qrcode/form/', views.QRCodeFormView.as_view(), name='create_qr_code_form'),
    path('<int:pk>/survey/stop/', views.SurveyStoppedView.as_view(), name='survey_stop'),
    path('<int:pk>/survey/pused/', views.SurveyPusedView.as_view(), name='survey_pused'),
    path('<int:pk>/survey/end/', views.EndSurveyView.as_view(), name='survey_end'),
]
