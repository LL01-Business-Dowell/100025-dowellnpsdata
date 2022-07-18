from django.views.generic import View
from django.shortcuts import render

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
