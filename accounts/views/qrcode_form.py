from django.views.generic import View
from django.shortcuts import render, redirect

from api.models import QrCode


class QRCodeFormView(View):
    template_name = 'qrcode/create_qr_code_form.html'
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
            checkbox = request.POST.get('checkbox')
            name = request.POST.get('name')
            email = request.POST.get('email')
            print(checkbox, name, email)
            qr_code.checkbox = checkbox
            qr_code.name = name
            qr_code.email = email
            qr_code.save()
            return redirect('survey_stop', qr_code.pk)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)


class SurveyStoppedView(View):
    template_name = 'qrcode/survey__stopped.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)


class SurveyPusedView(View):
    template_name = 'qrcode/survey__pused.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)


class EndSurveyView(View):
    template_name = 'qrcode/end_survey.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)
