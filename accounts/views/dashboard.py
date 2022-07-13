from django.shortcuts import render
import requests
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views.helper import upload_to_remote_db


class DashboardView(View):
    template_name = 'qrcode/feedback.html'

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

            url = 'http://' + host + '/api/qrcode/'
            res = requests.post(url, data=formdata, files=files)
            res_data = res.json()
            upload_to_remote_db(res_data)
            context = {
                'qrcode': res_data['qr_code'],
                'link': 'http://'+settings.HOSTNAME+'/iframe?url='+ res_data['url']

            }

            request.session['form_link'] = res_data['url']
            return render(request, 'qrcode/create_qr_code.html', context)
        context = {}
        return render(request, self.template_name, context)
