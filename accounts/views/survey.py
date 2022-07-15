from django.views.generic import View
from django.shortcuts import render

from api.models import QrCode


class SurveyDateView(View):
    template_name = 'qrcode/survey_date.html'
    model = QrCode

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        qr_code = self.model.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name)
