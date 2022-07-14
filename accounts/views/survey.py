from django.views.generic import View
from django.shortcuts import render


class SurveyDateView(View):
    template_name = 'qrcode/survey_date.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
