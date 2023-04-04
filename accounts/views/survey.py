from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.views.helper import get_survey_status, is_survey_owner_logged_in
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from api.models import QrCode


class SurveyDateView(View):
    template_name = 'qrcode/survey_date.html'
    model = QrCode
    @csrf_exempt
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)
        pause_survey = request.GET.get('pause_survey', '')

        if pause_survey:
            context = {
                'qr_code': qr_code,
                'pause_survey': True,
                'is_survey_owner_logged_in': is_survey_owner_logged_in(request, self.kwargs['pk'])
            }
        else:
            context = {
                'qr_code': qr_code,
                'is_survey_owner_logged_in': is_survey_owner_logged_in(request, self.kwargs['pk'])

            }

        return render(request, self.template_name, context)
    @csrf_exempt
    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            pause_survey = request.POST.get('pause_survey')
            print(start_date, end_date)

            if pause_survey == '1':
                qr_code.is_paused = True

            qr_code.start_date = start_date
            qr_code.end_date = end_date
            qr_code.save()
        context = {
            'qr_code': qr_code
        }

        if pause_survey == '1':
            return redirect('/my_surveys')

        # return render(request, self.template_name, context)
        return redirect('create_qr_code_form', qr_code.pk)

class MySurveysView(View):
    template_name = 'qrcode/my_surveys.html'
    model = QrCode
    @csrf_exempt
    @xframe_options_exempt
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
    @csrf_exempt
    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        pass

