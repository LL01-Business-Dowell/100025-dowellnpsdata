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
    return response


class DashboardView(View):
    template_name = 'qrcode/feedback.html'

    def get(self, request, *args, **kwargs):
        session = request.GET.get("session_id", None)
        if session:
            user = get_user_profile(session)
            if user:
                context = {}
                return render(request, self.template_name, context)
            else:
                context = {}
                # return redirect("https://100014.pythonanywhere.com/")
                return render(request, self.template_name, context)
        else:
            context = {}
            # return redirect("https://100014.pythonanywhere.com/")
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

            url = 'http://' + host + '/api/qrcode/'
            res = requests.post(url, data=formdata, files=files)
            res_data = res.json()
            upload_to_remote_db(res_data)
            context = {
                'qrcode': res_data['qr_code'],
                'pk': res_data['id'],
                'link': 'http://'+settings.HOSTNAME+'/iframe?url='+ res_data['url']

            }
            print('returning data')

            request.session['form_link'] = res_data['url']
            return render(request, 'qrcode/create_qr_code.html', context)
        context = {}
        return render(request, self.template_name, context)
