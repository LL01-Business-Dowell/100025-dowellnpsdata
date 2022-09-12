from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse

from api.models import QrCode


class SurveyDateView(View):
    template_name = 'qrcode/survey_date.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            print(start_date, end_date)
            qr_code.start_date = start_date
            qr_code.end_date = end_date
            qr_code.save()
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)

class MySurveysView(View):
    template_name = 'qrcode/to____be____set____later.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        
        # check if user is logged in first
        if 'username' not in request.session:
            return redirect("https://100014.pythonanywhere.com/")

        username = request.session['username']
        qr_codes = self.model.objects.filter(username=username)

        foo_response = ''

        for qr_code in qr_codes:
            foo_response += f'{qr_code.brand_name}\t {qr_code.start_date}\t {qr_code.promotional_sentence}<br>' 


        context = {
            'qr_codes': qr_codes
        }

        # return render(request, self.template_name, context)
        return HttpResponse(foo_response)

    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        pass

