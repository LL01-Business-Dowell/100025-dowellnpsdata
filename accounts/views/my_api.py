from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from datetime import datetime, date
from accounts.views.helper import upload_to_remote_db
from api.serializers import *
# from api.serializers import ListQrCodeSerializer, CreateQrCodeSerializer
# from api.models import QrCode
from django.conf import settings
class CustomError(Exception):
    pass
def my_date(date_str):
    # date_str = '19-09-2024'
    # today = datetime.now()
    # current_date = date(today.year, today.month, today.day)
    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()
    # correct_date =  date(date_object.year, date_object.month, date_object.day)
    # print("correct_date > current_date", correct_date > current_date)
    # print("date_object < current_date", date_object < current_date)
    return date_object
class GetDowellSurvey(APIView):
    def get(self, request, format=None):
        return JsonResponse({"data":"Kindly use a POST request instead of GET"})
    def post(self, request, format=None):

        myDict = request.data
        print("mydict ===> ", myDict)
        # p_list = myDict['p_list']
        formdata = {}
        files = {}

        try:
            # formdata["logo"] = myDict["logo"]
            api_key = myDict['api_key']
            # api_key = "bda22d28-9c84-4fcd-a2d3-bd5b9039a8"
            company_id = myDict['company_id']
            formdata['logo'] = myDict['logo']
            formdata["brand_name"] = myDict["brand_name"]
            formdata["service"] = myDict["service"]
            formdata["url"] = myDict["url"]
            formdata["country"] = myDict.getlist("country")
            formdata["region"] =myDict.getlist("region")
            formdata["promotional_sentence"] = myDict["promotional_sentence"]
            formdata["username"] = myDict["username"]
            formdata["name"] = myDict["name"]
            formdata["email"] = myDict["email"]
            formdata["start_date"] = my_date(myDict["start_date"])
            formdata["end_date"] = my_date(myDict["end_date"])
            host = request.META['HTTP_HOST']
            dta = formdata["country"]
            c = '-'.join(dta)
            formdata["country"] = c


            dta2 = formdata['region']
            r = '-'.join(dta2)
            formdata['region'] = r
            url = 'https://' + host + '/api/qrcode/'
            print("formdata ", formdata)
            print("url ", url)

            # serializer = QrCodeFileSerializer(data=request.data)
            serializer = CreateQrCodeSerializer(data=formdata)
            if serializer.is_valid():
                res = serializer.save()
                print("res", res)
                print("serializer", serializer.data)
                res_data = serializer.data

                upload_to_remote_db(res_data)
                # file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                # return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
                context = {
                        'qrcode': res_data['qr_code'],
                        'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id='+ str( res_data['id'])

                    }
                qrcode_type = "Link"
                quantity = 1
                company_id = company_id
                # files["logo"] = formdata['logo']
                link = 'https://'+settings.HOSTNAME+'/iframe?survey_id='+ str( res_data['id'])
                description = res_data['promotional_sentence']
                created_by = res_data['username']
                # api_key = "bda22d28-9c84-4fcd-a2d3-bd5b9039a8"
                # api_key = "d649ce60-7577-4eeb-8c86-fe591679cdcc"
                qrcode_url =  'https://100099.pythonanywhere.com/api/v2/qr-code/?api_key=' +api_key
                payload = {"qrcode_type":qrcode_type,
                    "quantity":quantity,
                    "company_id":company_id,
                    # "logo":logo,
                    "link":link,
                    "description":description,
                    "created_by":created_by}
                headers={"Content-Type": "multipart/form-data"}

                print("files === ",files)
                res = requests.post(qrcode_url, data=payload)
                # res = {"qr_code_generator_response": res}
                print("res === ",res)
                print("res.text === ",res.text)
                print("type res.text === ",type(res.text))
                res_obj = json.loads(res.text)
                print("res_obj === ",res_obj)

                return Response(res_obj,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # res = requests.get(url, data=formdata, files=files)



        except CustomError:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
