from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from datetime import datetime, date
from accounts.views.helper import upload_to_remote_db
from api.serializers import *
from api.models import QrCode

from django.conf import settings


import requests
from urllib.parse import urlparse, parse_qs


class CustomError(Exception):
    pass


def my_date(date_str):

    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_object


def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    print('url for checking api_key', url)
    payload = {
        "service_id": "DOWELL10016"
    }

    response = requests.post(url, json=payload)
    print(f"This is the response text {response.text}")
    print("Response Status Code:", response.status_code)
    return response


class GetDowellSurvey(APIView):
    def get(self, request, format=None):
        return JsonResponse({"data": "Kindly use a POST request instead of GET"})

    def post(self, request, format=None):

        myDict = request.data
        print("mydict ===> ", myDict)
        # p_list = myDict['p_list']
        formdata = {}
        files = {}

        try:
            api_key = request.query_params.get('api_key')
            print('This is the params api', api_key)
            # process_api_response = processApikey(api_key)
            # if process_api_response.status_code == 200:
            process_api_response = api_key
            if process_api_response == '76092219-c570-4c86-88f0-efa63966e06b':
                print('This is the api_key response', process_api_response)
                company_id = myDict['company_id']
                formdata['logo'] = myDict['logo']
                formdata["brand_name"] = myDict["brand_name"]
                formdata["service"] = myDict["service"]
                formdata["url"] = myDict["url"]
                formdata["country"] = myDict.getlist("country")
                formdata["region"] = myDict.getlist("region")
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
                # print("url ", url)

                # serializer = QrCodeFileSerializer(data=request.data)
                serializer = CreateQrCodeSerializer(data=formdata)
                if serializer.is_valid():
                    res = serializer.save()
                    print("this is the res data here", res)
                    # print("serializer", serializer.data)
                    res_data = serializer.data

                    upload_to_remote_db(res_data)
                    # file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
                    # return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
                    
                    context = {
                        'qrcode': res_data['qr_code'],
                        'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id=' + str(res_data['id'])

                    }
                    
                    qrcode_type = "Link"
                    quantity = 1
                    company_id = company_id
                    link = 'https://'+settings.HOSTNAME + \
                        '/iframe?survey_id=' + str(res_data['id'])
                    description = res_data['promotional_sentence']
                    created_by = res_data['username']

                    qrcode_url = 'https://www.qrcodereviews.uxlivinglab.online/api/v2/qr-code/?api_key=' + api_key
                    payload = {"qrcode_type": qrcode_type,
                            "quantity": quantity,
                            "company_id": company_id,
                            # "logo":logo,
                            "link": link,
                            "description": description,
                            "created_by": created_by}
                    headers = {"Content-Type": "multipart/form-data"}

                    print("files === ", files)
                    res = requests.post(qrcode_url, data=payload)
                    # res = {"qr_code_generator_response": res}
                    print("res === ", res)
                    print("res.text === ", res.text)
                    print("type res.text === ", type(res.text))
                    res_obj = json.loads(res.text)
                    print("res_obj === ", res_obj)

                    return Response(res_obj, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("API Key validation failed.", status=status.HTTP_400_BAD_REQUEST)
            
            # res = requests.get(url, data=formdata, files=files)

        except CustomError:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, qrcode_id, format=None):
        myDict = request.data
        print("mydict ===> ", myDict)
        # p_list = myDict['p_list']
        formdata = {}
        files = {}
    
        try:
            try:
                qrcode_survey_id = qrcode_id
                response = requests.get(f"https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_survey_id}/")
                response_json = response.json()
                link = response_json["response"][0]["link"]
                parsed_url = urlparse(link)
                query_params = parse_qs(parsed_url.query)
                survey_id = query_params.get("survey_id")[0] if "survey_id" in query_params else None
                print(f"Link found {link}")
                print(f"Survey Id from the link {survey_id}")
                survey = QrCode.objects.get(id=survey_id)
            except QrCode.DoesNotExist:
                raise Http404("Survey not found")
            
            
            formdata = {}
            files = {}
            api_key = request.query_params.get('api_key')
            # process_api_response = processApikey(api_key)
            # if process_api_response.status_code == 200:
            process_api_response = api_key
            if process_api_response == '76092219-c570-4c86-88f0-efa63966e06b':
                company_id = myDict['company_id']
                description = myDict['description']
                qrcode_color = myDict["qrcode_color"]
                formdata['logo'] = myDict['logo']
                link = myDict["link"]
                created_by = myDict["created_by"]
                host = request.META['HTTP_HOST']
                
                
                formdata["brand_name"] = myDict["brand_name"]
                formdata["service"] = myDict["service"]
                formdata["url"] = myDict["url"]
                formdata["country"] = myDict.getlist("country")
                print('country', formdata['brand_name'])
                formdata["region"] = myDict.getlist("region")
                formdata["promotional_sentence"] = myDict["promotional_sentence"]
                formdata["username"] = myDict["username"]
                formdata["name"] = myDict["name"]
                formdata["email"] = myDict["email"]
                formdata["start_date"] = my_date(myDict["start_date"])
                formdata["end_date"] = my_date(myDict["end_date"])
                # ====================================
                
                
                serializer = UpdateQrCodeSerializer(survey,data=formdata)
                if serializer.is_valid():
                    res = serializer.save()
                    res_data = serializer.data
                    update_to_remote_db(res_data)

                    logo = res_data['logo']
                    company_id = company_id
                    link = link
                    created_by = created_by
                    qrcode_color = qrcode_color
                    description = description
                   
                    
                    qrcode_url = f'https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_id}/?api_key=' + api_key
                    payload = {
                        "logo": logo,
                        "company_id": company_id,
                        "link": link,
                        "description": description,
                        "created_by": created_by,
                        "qrcode_color": qrcode_color,
                    }
                    headers = {"Content-Type": "multipart/form-data"}
                    res = requests.put(qrcode_url, data=payload)
                    res_obj = json.loads(res.text)
                    return Response(res_obj, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("API Key validation failed.", status=status.HTTP_400_BAD_REQUEST)
        except CustomError:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)   
    
    
    