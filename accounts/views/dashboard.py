from django.shortcuts import render, redirect
from api.serializers import *
import requests
import json
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views.helper import upload_to_remote_db
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

# from api.serializers import ListQrCodeSerializer, CreateQrCodeSerializer
def get_key():
    username = "dowellFeedback"
    password = "DOWELL@qrcode2022"
    URL = 'https://100014.pythonanywhere.com/api/login/'
    payload = {
        'username': username,
        'password': password,
    }
    response = requests.post(URL, data=payload)
    print(response)
    return response.json()

def get_user_profile(session):
    data = {'key': session}
    headers = {"Content-Type": "application/json"}
    url = "https://100014.pythonanywhere.com/api/profile/"
    response = requests.post(url, data, headers)
    print("get_user_profile --> ",response.json())
    return response.json()


class DashboardView(View):
    template_name = 'qrcode/feedback.html'
    @csrf_exempt
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        session = request.GET.get("session_id", None)
        # james test session id
        # uncomment below lines before uploading to live server
        # session = 'gt4j8zr8zfvh0go1e2v3fh2sibe9diw9'
        #return render(request, self.template_name, {})

        # if user is already logged-in in session don't redirect to login page
        # if session or 'user' in request.session:
        #     if session:
        #         user = get_user_profile(session)
        #     else:
        #         user = request.session['user']
        #     if user:
        #         # save customers username and user profile to session
        #         request.session['username'] = user['username']
        #         request.session['user'] = user
        #         #context = {}
        #         context = {
        #             'user': user,
        #             'session_id': session
        #         }
        #         return render(request, self.template_name, context)
        #     else:
        #         context = {}
        #         return redirect("https://100014.pythonanywhere.com/")
        # else:
        #     context = {}
        #     return redirect("https://100014.pythonanywhere.com/")
        if session:
            user = get_user_profile(session)
            if user:
                # save customers username and user profile to session
                request.session['username'] = user['username']
                request.session['user'] = user
                #context = {}
                context = {
                    'user': user,
                    'session_id': session
                }
                return render(request, self.template_name, context)
            else:
                context = {}
                # return redirect("https://100014.pythonanywhere.com/")
                return redirect("https://100014.pythonanywhere.com/?redirect_url=https://100025.pythonanywhere.com/")
        else:
            context = {}
            # return redirect("https://100014.pythonanywhere.com/")
            return redirect("https://100014.pythonanywhere.com/?redirect_url=https://100025.pythonanywhere.com/")
    @csrf_exempt
    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.FILES:
            # check if user is logged in first
            print("request.session --> ",request.session['username'])
            for key, value in request.session.items():
                print(f"Key: {key}, Value: {value}")
            for key in request.session.keys():
                print(f"Key: {key}")
            if 'username' not in request.session.keys():
                print("username not in request.session.keys()",request.session.keys())
                return redirect("https://100014.pythonanywhere.com/")
            else:
                print("username IN request.session.keys()",request.session.keys())

            # headers = {
            #     "cache-control": "no-cache",
            # }

            formdata = {}

            # formdata['logo'] = request.FILES['logo'].file.getvalue()
            files = {'logo': request.FILES['logo']}
            formdata['logo'] =request.FILES['logo']
            formdata['brand_name'] = request.POST.get('brand_name')
            formdata['service'] = request.POST.getlist('service')
            formdata['url'] = request.POST.get('url')
            formdata['country'] = request.POST.getlist('country')
            formdata['region'] = request.POST.getlist('regions')
            formdata['promotional_sentence'] = request.POST.get('promotional_sentence')
            formdata['username'] = request.session['username']
            host = request.META['HTTP_HOST']

            url = 'https://' + host + '/api/qrcode/'

            dta = formdata["country"]
            c = '-'.join(dta)
            formdata["country"] = c


            dta2 = formdata['region']
            r = '-'.join(dta2)
            formdata['region'] = r
            dta3 = formdata['service']
            s = '-'.join(dta3)
            formdata['service'] = s
            print("Serializer files type", type(files['logo']))
            print("Serializer files ", files)
            serializer = CreateQrCodeSerializer(data=formdata)
            if serializer.is_valid():
                serializer.save()
                # print("res", res)
                print("serializer", serializer.data)
                res_data = serializer.data

                upload_to_remote_db(res_data)
                # file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                # return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
                context = {
                'qrcode': res_data['qr_code'],
                'country': res_data['country'],
                'region': r,
                'promotional_sentence': res_data['promotional_sentence'],
                'pk': res_data['id'],
                'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+str(res_data['id'])

            }
                print(context, 'returning data')

                request.session['form_link'] = res_data['url']
                return render(request, 'qrcode/create_qr_code.html', context)
            else:
                print("SERIALIZER WAS NOT VALID")
                errors = serializer.errors
                print("errors are --> ",errors)
            # res = requests.post(url, data=formdata, files=files)


            # res_data = res.json()
            # upload_to_remote_db(res_data)

            # # added &survey_id='+res_data['id'] to include survey_id in the link in qrcode
            # context = {
            #     'qrcode': res_data['qr_code'],
            #     'country': res_data['country'],
            #     'region': r,
            #     'promotional_sentence': res_data['promotional_sentence'],
            #     'pk': res_data['id'],
            #     'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+str(res_data['id'])

            # }
            # print(context, 'returning data')

            # request.session['form_link'] = res_data['url']
            # return render(request, 'qrcode/create_qr_code.html', context)
        context = {}
        return render(request, self.template_name, context)
