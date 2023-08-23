from pyexpat import model
from rest_framework import serializers
import requests
import json
import traceback
import sys
from .models import QrCode
from PIL import Image
import qrcode
from django.conf import settings
import base64
# from accounts.views.helper import get_event_id
from django.conf import settings

def get_event_id():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r=requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else:
        return json.loads(r.text)['error']

# def decodeDesignImage(data):
#     try:
#         data = base64.b64decode(data.encode('UTF-8'))
#         buf = io.BytesIO(data)
#         img = Image.open(buf)
#         return img
#     except:
#         return None

class CreateQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        # exclude = ['qr_code',]
        fields = '__all__'

    def create(self, validated_data):
        try:
            new_qrcode = QrCode.objects.create(**validated_data)
            Logo_link = validated_data.pop('logo')
            filename = Logo_link.name

            logo = Image.open(Logo_link)
            basewidth = 100

            wpercent = (basewidth/float(logo.size[0]))
            hsize = int((float(logo.size[1])*float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)


            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )
            host = settings.HOSTNAME

            # url = validated_data.pop('url')
            survey_url = validated_data['url']

            url = 'https://' + host + '/iframe?survey_id='+ str(new_qrcode.id)
            print("url----------------------------->"+url)


            QRcode.add_data(url)


            QRcode.make()


            QRcolor = 'Black'

            # adding color to QR code
            QRimg = QRcode.make_image(
                fill_color=QRcolor, back_color="white").convert('RGB')

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)

            # box = Image.open('background.png')
            # QRimg.paste(box, pos)
            QRimg.paste(logo,pos)

            # QRimg.show()

            # save the QR code generated
            QRimg.save(settings.MEDIA_ROOT+'/company_qrcode/'+filename)
            filepath = 'company_qrcode/'+filename
            new_qrcode.qr_code = filepath
            with open(settings.MEDIA_ROOT+'/company_qrcode/'+filename, "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())



            new_qrcode.image = converted_string
            new_qrcode.event_id = get_event_id()
            new_qrcode.save()
            print("This is the validated data in serializer to be save", new_qrcode)
            return new_qrcode
        
        except Exception as ex:

            print("Exception is serializwe ", ex)
            print(ex, traceback.format_exc())
            
            
            
class UpdateQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            logo = validated_data.pop('logo')

            # Update the logo field of the existing instance
            instance.logo = logo
            instance.save()

            return instance
        except Exception as ex:
            print("Exception in serializer: ", ex)
            print(traceback.format_exc())
            raise ex

            # print(traceback.format_exc())
    # or
            # print(sys.exc_info()[2])



class ListQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = '__all__'