from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.views.helper import get_survey_status, is_survey_owner_logged_in

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
        # return render(request, self.template_name, context)
        return redirect('create_qr_code_form', qr_code.pk)

class MySurveysView(View):
    template_name = 'qrcode/my_surveys.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        
        # check if user is logged in first
        if 'username' not in request.session:
            return redirect("https://100014.pythonanywhere.com/")

        survey_id = request.GET.get('delete', '')
        message = ''

        if survey_id:
            try:
                qr_code = self.model.objects.get(pk=survey_id)

                if is_survey_owner_logged_in(request, survey_id):
                    qr_code.delete()
                    message = 'Survey deleted Successfully'
            except:
                pass
            


        username = request.session['username']
        qr_codes = self.model.objects.filter(username=username)

        for qr_code in qr_codes:
            survey_status, survey_link, survey_link_text = get_survey_status(qr_code.id)
            qr_code.survey_status = survey_status
            qr_code.survey_link = survey_link
            qr_code.survey_link_text = survey_link_text

        context = {
            'qr_codes': qr_codes,
            'message': message
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        pass

