from django.shortcuts import render, redirect
import requests
import json
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views.helper import upload_to_remote_db


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
    print(response)
    return response.json()


class DashboardView(View):
    template_name = 'qrcode/feedback.html'

    def get(self, request, *args, **kwargs):
        session = request.GET.get("session_id", None)
        # james test session id
        # uncomment below lines before uploading to live server
        session = 'gt4j8zr8zfvh0go1e2v3fh2sibe9diw9'
        #return render(request, self.template_name, {})

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
                return redirect("https://100014.pythonanywhere.com/")
        else:
            context = {}
            return redirect("https://100014.pythonanywhere.com/")

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.FILES:
            # check if user is logged in first
            if 'username' not in request.session:
                return redirect("https://100014.pythonanywhere.com/")

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
            formdata['username'] = request.session['username']
            host = request.META['HTTP_HOST']

            url = 'http://' + host + '/api/qrcode/'
            res = requests.post(url, data=formdata, files=files)
            res_data = res.json()
            upload_to_remote_db(res_data)
            
            # added &survey_id='+res_data['id'] to include survey_id in the link in qrcode
            context = {
                'qrcode': res_data['qr_code'],
                'promotional_sentence': res_data['promotional_sentence'],
                'pk': res_data['id'],
                'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+str(res_data['id'])

            }
            print('returning data')

            request.session['form_link'] = res_data['url']
            return render(request, 'qrcode/create_qr_code.html', context)
        context = {}
        return render(request, self.template_name, context)
