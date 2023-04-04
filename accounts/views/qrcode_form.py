from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from api.models import QrCode

# this is the mail 
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .email_handler import mail_sender


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
            print("hdihsihishdi")
            print(qr_code.qr_code)
            print(str(qr_code.qr_code))
            qr_code.checkbox = checkbox
            qr_code.name = name
            qr_code.email = email
            qr_code.save()


            # message = 'DOWELL RESEARCH'
            # html_template = 'qrcode/email__template.html'
            # html_msg =  render_to_string(html_template)
            # subject = 'welcome to the dowell'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [qr_code.email]
            # message = EmailMessage(subject, html_msg, email_from, recipient_list)
            # host = request.META['HTTP_HOST']
            host = settings.HOSTNAME

            qr_code_src = 'https://' + host + '/media/'+str(qr_code.qr_code)
            data_survey_id =  qr_code.id
            survey_title =  qr_code.brand_name
            user_name = qr_code.username
            res = mail_sender(email, name,qr_code_src, data_survey_id,survey_title, user_name )
            # message.content_subtype = 'html'
            # message.send()
            print("mail send")
            
            # display email form to be sent to user
            # context = {
            #     'qr_code': qr_code
            # }
            # return render(request, 'qrcode/email__template.html', context)

            if not res['error']:
                return redirect(f'/my_surveys')
            else:
                context = {
            'qr_code': qr_code,
            'Error': res['status']
        }
            return render(request, self.template_name, context)
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)


class SurveyPreviewEmailView(View):
    template_name = 'qrcode/email__template.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        survey_id = request.GET.get('survey_id', '')
        qr_code = get_object_or_404(QrCode, pk=survey_id)
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

    def post(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        if request.method == 'POST':
            reason = request.POST.get('reason')
            print(reason)
            qr_code.is_paused = True
            qr_code.save()
            return redirect('survey_pused', qr_code.pk)
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
            return redirect('/my_surveys')
        context = {
            'qr_code': qr_code
        }
        return render(request, self.template_name, context)
