from django.views.generic import View
from django.shortcuts import render, redirect

from api.models import QrCode


class QRCodeFormView(View):
    template_name = 'qrcode/create_qr_code_form.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        print(qr_code.start_date, qr_code.end_date)

        if 'user' in request.session:
            qr_code.name = request.session['user']['first_name'] + ' ' + request.session['user']['last_name']
            qr_code.email = request.session['user']['email']
        else:
            qr_code.name = ''
            qr_code.email = ''

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
            
            # display email form to be sent to user
            context = {
                'qr_code': qr_code
            }
            return render(request, 'qrcode/email__template.html', context)


            return redirect(f'/iframe/?survey_id={qr_code.pk}')
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


class SurveyStartView(View):
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        qr_code.is_end = False
        qr_code.is_paused = False
        qr_code.reason = ''
        qr_code.save()
        return redirect("survey_end", qr_code.pk)


class SurveyPusedView(View):
    template_name = 'qrcode/survey_pused.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        qr_code.is_paused = True
        qr_code.save()
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

    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        if request.method == 'POST':
            reason = request.POST.get('reason')
            print(reason)
            qr_code.reason = reason
            qr_code.is_end = True
            qr_code.save()
            return redirect('survey_pused', qr_code.pk)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)
