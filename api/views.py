from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ListQrCodeSerializer, CreateQrCodeSerializer
from .models import QrCode
from django.conf import settings

from django.contrib.sites.models import Site






# import modules
import qrcode
from PIL import Image

    


class QrCodeViewSet(viewsets.ModelViewSet):
    
    queryset = QrCode.objects.all()


    def get_serializer_class(self):
        if self.action == 'create':
            return CreateQrCodeSerializer
        if self.action == 'retrive':
            return ListQrCodeSerializer
        return ListQrCodeSerializer

    # def create(self, request):
    #     print('from api')
    #     print(request.data)
    
    

    

