from django.shortcuts import render
import requests
from rest_framework.response import Response

# Create your views here.


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
        
        

        url ='http://'+host+'/api/qrcode/'
        res = requests.post(url, data = formdata, files=files)
        res_data = res.json()
        context ={
            'qrcode': res_data['qr_code'],
            
        }

        request.session['form_link'] = res_data['url']
        return render(request, 'qrcode.html', context)

    return render(request, 'form.html')

def render_qrcode(request):
    return render(request,'qrcode.html')


def render_iframe(request):
    context = {
        'url_link':request.session['form_link']
    }
    return render(request, 'iframe.html',context )