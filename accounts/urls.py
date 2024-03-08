from django.shortcuts import render
from django.urls import path, include
from accounts.views.helper import render_form, render_qrcode, render_iframe, get_event_id
from accounts.views.my_api import GetDowellSurvey
from accounts.views.my_apiV2 import GetDowellSurvey as GetDowellSurveyV2
from accounts.views.my_apiV2 import ExtractAndFetchSurvey, SurveyCounter, MySurveyFetch
from accounts import views
from accounts.views import health_check_views

urlpatterns = [
    path('login/', views.LoInFunc.as_view(), name='login'),
    path('form/', render_form, name='form'),

    # path('test', text_qrcode_page),

    path('get_eventid', get_event_id, name='get_event_id'),
    path('qrcode', render_qrcode, name='qrcode'),
    path('iframe/', render_iframe, name='iframe'),
    path('my_surveys/', views.MySurveysView.as_view(), name='my_surveys'),
    path('preview_email/', views.SurveyPreviewEmailView.as_view(), name='preview_email'),
    path('', views.DashboardView.as_view(), name='feedback'),
    path('<int:pk>/set/survey/date/', views.SurveyDateView.as_view(), name='set_survey_date'),
    path('<int:pk>/create/qrcode/form/', views.QRCodeFormView.as_view(), name='create_qr_code_form'),
    path('<int:pk>/survey/stop/', views.SurveyStoppedView.as_view(), name='survey_stop'),
    path('<int:pk>/survey/pused/', views.SurveyPusedView.as_view(), name='survey_pused'),
    path('<int:pk>/survey/end/', views.EndSurveyView.as_view(), name='survey_end'),
    path('<int:pk>/survey/start/', views.SurveyStartView.as_view(), name='survey_start'),
    ###my api paths
    path('get-survey/', GetDowellSurvey.as_view(), name='get-survey'),
    path('update-qr-code/<int:qrcode_id>/', GetDowellSurvey.as_view(), name='update-survey'),
    ###my api v2 paths
    path('create-surveyv2', GetDowellSurveyV2.as_view(), name='get-surveyv2'),
    path('update-qr-codev2', GetDowellSurveyV2.as_view(), name='update-surveyv2'),
    path('get-dowell-survey-status/', ExtractAndFetchSurvey.as_view(), name='get_dowell_survey'),
    path('survey-count/', SurveyCounter.as_view(), name='survey-counter'),
    ##health_check
    path('health-check/', health_check_views.HealthCheck.as_view(), name='health-check'),
    path('my-survey/', MySurveyFetch.as_view()),
]
