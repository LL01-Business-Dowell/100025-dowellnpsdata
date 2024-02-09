
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt # add this
@method_decorator(csrf_exempt, name='dispatch')
class HealthCheck(APIView):
    def get(self, request ):
        return Response("Sever is running fine",status=status.HTTP_200_OK)