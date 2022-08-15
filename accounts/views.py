from django.shortcuts import render, redirect
import sys
import requests
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from accounts.login import get_user_profile

def text_qrcode_page(request):
    return render(request, 'proceed.html')

def render_form(request):
    try:
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
            print("host")
            print(host)
            url = 'https://' + host + '/api/qrcode/'
            print("url")
            print(url)
            res = requests.post(url, data=formdata, files=files)
            print("res")
            print(res)
            print("settings.HOSTNAME")
            print(settings.HOSTNAME)
            res_data = res.json()

            upload_to_remote_db(res_data)
            context = {
                'qrcode': res_data['qr_code'],
                'link': 'https://'+settings.HOSTNAME+'/iframe?url='+ res_data['url']

            }

            request.session['form_link'] = res_data['url']
            return render(request, 'qrcode.html', context)
    except Exception as err:
            print("Ecxetption Err")
            # print(sys.exc_info())
            # print(err, traceback.format_exc())
    session = request.GET.get("session_id", None)
    if session:
        user = get_user_profile(session)
        print("Userrrr ------------->>>>>>")
        print(session)
        print(type(user))
        print(user)

        if user is None:
            return redirect("https://100014.pythonanywhere.com/")
        else:
            return render(request, 'form.html')

    else:
        return redirect("https://100014.pythonanywhere.com/")



def home(request):
    session = request.GET.get("session_id", None)
    if session:
        user = get_user_profile(session)

        if user is None:
            return redirect("https://100014.pythonanywhere.com/")
        else:
            return render(request, 'form.html')


    else:
        return redirect("https://100014.pythonanywhere.com/")

def render_qrcode(request):
    return render(request, 'qrcode.html')


def render_iframe(request):
    survey_link = request.GET.get('url', '')
    if survey_link:
        url_link = survey_link
    else:
        url_link= request.session['form_link']
    context = {
        'url_link': url_link
        # 'url_link': request.session['form_link']
    }
    return render(request, 'iframe.html', context)


def get_event_id():
    dd = datetime.now()
    time = dd.strftime("%d:%m:%Y,%H:%M:%S")
    url = "https://100003.pythonanywhere.com/event_creation"
    data = {"platformcode": "FB", "citycode": "101", "daycode": "0",
            "dbcode": "pfm", "ip_address": "192.168.0.41",
            "login_id": "lav", "session_id": "new",
            "processcode": "1", "regional_time": time,
            "dowell_time": time, "location": "22446576",
            "objectcode": "1", "instancecode": "100051", "context": "afdafa ",
            "document_id": "3004", "rules": "some rules", "status": "work"
            }

    r = requests.post(url, json=data)
    return r.text


def upload_to_remote_db(data):
    # print('sanity check')
    # print(data)
    url = "http://100002.pythonanywhere.com/"
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
    print(response.text)
