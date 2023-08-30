from django.shortcuts import render, get_object_or_404
import requests
from rest_framework.response import Response
from datetime import datetime, date
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from api.models import QrCode


def text_qrcode_page(request):
    return render(request, 'proceed.html')

def render_form(request):
    if request.method == 'POST' and request.FILES:
        headers = {
            "cache-control": "no-cache",
        }

        formdata = {}

        # formdata['logo'] = request.FILES['logo'].file.getvalue()
        files = {'logo': request.FILES['logo']}
        formdata['brand_name'] = request.POST.get('brand_name')
        formdata['service'] = request.POST.get('service')
        formdata['url'] = request.POST.get('url')
        formdata['location'] = request.POST.get('location')
        formdata['promotional_sentence'] = request.POST.get('promotional_sentence')
        host = request.META['HTTP_HOST']

        url = 'https://' + host + '/api/qrcode/'
        res = requests.post(url, data=formdata, files=files)
        res_data = res.json()

        upload_to_remote_db(res_data)
        context = {
            'qrcode': res_data['qr_code'],
            'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+ res_data['id']

        }

        request.session['form_link'] = res_data['url']
        return render(request, 'qrcode.html', context)

    return render(request, 'form.html')


def render_qrcode(request):
    return render(request, 'qrcode.html')


# def render_iframe(request):
#     survey_link = request.GET.get('url', '')
#     # qr_code = QrCode.objects.filter(url=survey_link)[0]
#     # print(qr_code)
#     current_date = datetime.now()
#     print(current_date)
#     if survey_link:
#         url_link = survey_link
#     else:
#         url_link= request.session['form_link']
#     context = {
#         'url_link': url_link
#         # 'url_link': request.session['form_link']
#     }
#     return render(request, 'iframe.html', context)


def render_iframe(request):
    survey_id = request.GET.get('survey_id', '')
    qr_code = get_object_or_404(QrCode, pk=survey_id)

    a = qr_code.country
    country = a.split("-")
    print(country)

    r = qr_code.region
    region = r.split("-")
    print(region)

    today = datetime.now()
    current_date = date(today.year, today.month, today.day)
    message = ''
    if qr_code.is_end:
        context = {
            'message': 'Survey was stopped because '+qr_code.reason,
            'brand_name': qr_code.brand_name,
            'qr_code': qr_code,
            'status_image': 'endsurvey2.png',
            'start_survey': is_survey_owner_logged_in(request, survey_id),
            'country': country,
            'region': region

        }
        return render(request, 'qrcode/survey_not_started.html', context)
    if qr_code.is_paused:
        context = {
            'message': 'Survey has been paused',
            'brand_name': qr_code.brand_name,
            'qr_code': qr_code,
            'status_image': 'endsurvey.png',
            'resume_survey': is_survey_owner_logged_in(request, survey_id),
            'country': country,
            'region': region
        }
        return render(request, 'qrcode/survey_not_started.html', context)
    if qr_code.start_date and qr_code.end_date:
        if qr_code.start_date <= current_date <= qr_code.end_date:
            survey_url = qr_code.url
        else:
            if qr_code.start_date > current_date:
                survey_url = None
                message = 'Survey will start on '+str(qr_code.start_date)
                context = {
                    'message': message,
                    'brand_name': qr_code.brand_name,
                    'qr_code': qr_code,
                    'status_image': 'checklist.png',
                    'edit_dates': is_survey_owner_logged_in(request, survey_id),
                    'country': country,
                    'region': region
                }
                return render(request, 'qrcode/survey_not_started.html', context)
            else:
                survey_url = None
                message = "Survey ended on "+str(qr_code.end_date)
                context = {
                    'message': message,
                    'brand_name': qr_code.brand_name,
                    'qr_code': qr_code,
                    'status_image': 'checklist.png',
                    'edit_dates': is_survey_owner_logged_in(request, survey_id),
                    'country': country,
                    'region': region


                }
                return render(request, 'qrcode/survey_not_started.html', context)
    else:
        survey_url = None
        message = "Survey date is not set yet."
        context = {
            'message': message,
            'qr_code': qr_code,
            'status_image': 'checklist.png',
            'edit_dates': is_survey_owner_logged_in(request, survey_id),
            'country': country,
            'region': region

        }
        return render(request, 'qrcode/survey_not_started.html', context)

    # check if logged in user is the one who uploaded this survey
    username = request.session.get('username', '')
    if username == qr_code.username:
        manage_survey = True
    else:
        manage_survey = False
    if username == '':
        manage_survey = False

    context = {
        'survey_url': survey_url,
        'message': message,
        'qr_code': qr_code,
        'manage_survey': manage_survey,
        'country': country,
        'region': region
    }
    return render(request, 'iframe.html', context)


def get_survey_status(survey_id):
    survey_status = 'Survey Ongoing'
    survey_link = f'/iframe/?survey_id={survey_id}'
    survey_link_text = 'Fill Survey'

    qr_code = get_object_or_404(QrCode, pk=survey_id)
    today = datetime.now()
    current_date = date(today.year, today.month, today.day)
    message = ''
    if qr_code.is_end:
        survey_status = 'Survey Ended'
        survey_link_text = 'Start Survey'
        survey_link = f'/{survey_id}/survey/start/'
    elif qr_code.is_paused:
        survey_status = f'Survey paused until {qr_code.start_date}'
        survey_link_text = 'Resume Survey'
        survey_link = f'/{survey_id}/survey/start/'
    elif qr_code.start_date and qr_code.end_date:
        if qr_code.start_date <= current_date <= qr_code.end_date:
            survey_url = qr_code.url
        else:
            if qr_code.start_date > current_date:
                survey_status = 'Not started'
                survey_link_text = 'Edit dates'
                survey_link = f'/{survey_id}/set/survey/date/'
            else:
                survey_status = 'Survey Ended'
                survey_link_text = 'Extend date'
                survey_link = f'/{survey_id}/set/survey/date/'
    else:
        survey_status = 'Date not set'
        survey_link_text = 'Set dates'
        survey_link = f'/{survey_id}/set/survey/date/'

    return survey_status, survey_link, survey_link_text

# def get_event_id():
#     dd = datetime.now()
#     time = dd.strftime("%d:%m:%Y,%H:%M:%S")
#     url = "https://100003.pythonanywhere.com/event_creation"
#     data = {"platformcode": "FB", "citycode": "101", "daycode": "0",
#             "dbcode": "pfm", "ip_address": "192.168.0.41",
#             "login_id": "lav", "session_id": "new",
#             "processcode": "1", "regional_time": time,
#             "dowell_time": time, "location": "22446576",
#             "objectcode": "1", "instancecode": "100051", "context": "afdafa ",
#             "document_id": "3004", "rules": "some rules", "status": "work"
#             }

#     r = requests.post(url, json=data)
#     return r.text
def get_event_id():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r=requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else:
        return json.loads(r.text)['error']


def is_survey_owner_logged_in(request, survey_id):
    if 'username' in request.session:
        model = QrCode
        qr_code = model.objects.get(pk=survey_id)
        if qr_code.username == request.session['username']:
            return True
    return False


def upload_to_remote_db(data):
    # print('sanity check')
    # print(data)
    url = "https://100002.pythonanywhere.com/"
    # searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = {
        "cluster": "nps",

        "database": "voc_survey",

        "collection": "client_voc_data",

        "document": "client_voc_data",

        "team_member_ID": "76888881",

        "function_ID": "ABCDE",

        "command": "insert",

        "field": data,
        "update_field": {
            "order_nos": 21
        },
        "platform": "bangalore"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)
    print('this is the response from the remote db', response.text, 'the data is ', data)

def update_to_remote_db(data):
    # print('sanity check')
    # print(data)
    url = "https://100002.pythonanywhere.com/"
  
    # searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = {
        "cluster": "nps",

        "database": "voc_survey",

        "collection": "client_voc_data",

        "document": "client_voc_data",

        "team_member_ID": "76888881",

        "function_ID": "ABCDE",

        "command": "update",

        "field": data,
        "update_data": data,
        "update_field": {
            "order_nos": 21
        },
        "platform": "bangalore"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)
    # print('The update response from mongo Db is ', response.text, 'and this is the data ', data)
    
    
class FeedbackView(View):
    template_name = 'dashboard/feedback.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.FILES:

            headers = {
                "cache-control": "no-cache",
            }

            formdata = {}

            # formdata['logo'] = request.FILES['logo'].file.getvalue()
            files = {'logo': request.FILES['logo']}
            formdata['brand_name'] = request.POST.get('brand_name')
            formdata['service'] = request.POST.get('service')
            formdata['url'] = request.POST.get('url')
            formdata['location'] = request.POST.get('location')
            formdata['promotional_sentence'] = request.POST.get('promotional_sentence')
            host = request.META['HTTP_HOST']

            url = 'https://' + host + '/api/qrcode/'
            res = requests.post(url, data=formdata, files=files)
            res_data = res.json()
            upload_to_remote_db(res_data)
            context = {
                'qrcode': res_data['qr_code'],
                'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+ res_data['id']

            }

            request.session['form_link'] = res_data['url']
            return render(request, 'qrcode.html', context)
        context = {}
        return render(request, self.template_name, context)