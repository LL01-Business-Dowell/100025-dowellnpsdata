from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from datetime import datetime, date
from accounts.views.helper import upload_to_remote_db, update_to_remote_db
from api.serializers import *
from api.models import QrCode, QrCodeV2


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
            # process_api_response = api_key
            # if process_api_response == '76092219-c570-4c86-88f0-efa63966e06b':
            process_api_response = processApikey(api_key)
            if process_api_response.status_code == 200:
                print('This is the api_key response', process_api_response)
                company_id = myDict['company_id']
                formdata['logo'] = myDict['logo']
                formdata["brand_name"] = myDict["brand_name"]
                formdata["service"] = myDict.getlist("service")
                formdata["url"] = myDict["url"]
                formdata["country"] = myDict.getlist("country")
                formdata["region"] = myDict.getlist("region")
                formdata["promotional_sentence"] = myDict["promotional_sentence"]
                formdata["username"] = myDict["username"]
                formdata["name"] = myDict["name"]
                formdata["email"] = myDict["email"]
                # formdata["participantsLimit"] = myDict["participantsLimit"]
                formdata["participantsLimit"] = myDict.get("participantsLimit", {})
                formdata["link"] = myDict["link"]
                formdata["start_date"] = my_date(myDict["start_date"])
                print('Date printier ', formdata["start_date"])
                formdata["end_date"] = my_date(myDict["end_date"])
                host = request.META['HTTP_HOST']
                dta = formdata["country"]
                c = '-'.join(dta)
                formdata["country"] = c

                dta2 = formdata['region']
                r = '-'.join(dta2)
                formdata['region'] = r

                dta3 = formdata['service']
                k = '-'.join(dta3)
                formdata['service'] = k

                url = 'https://' + host + '/api/qrcode/'
                print("formdata printier", formdata)
                
                print('Serialize this ', formdata)
                serializer = CreateQrCodeSerializerV2(data=formdata)
                if serializer.is_valid():
                    res = serializer.save()
                    print("this is the res data here", res)
                    # print("serializer", serializer.data)
                    res_data = serializer.data

                    upload_to_remote_db(res_data)


                    return Response(res_data, status=status.HTTP_200_OK)
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
                print('qrcode_survey_id is ', qrcode_survey_id)
                responses = requests.get(
                    f"https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_survey_id}/")
                print('The link for upload ', responses.text)
                response_json = responses.json()
                links = response_json["response"][0]["link"]
                parsed_url = urlparse(links)
                query_params = parse_qs(parsed_url.query)
                survey_id = query_params.get("survey_id")[
                    0] if "survey_id" in query_params else None
                print(f"Links found {links}")
                print(f"Survey Id from the link {survey_id}")
                survey = QrCodeV2.objects.get(id=survey_id)
            except QrCodeV2.DoesNotExist:
                raise Http404("Survey not found")

            for key, value in myDict.items():
                if value:  # Check if the value is not empty
                    formdata[key] = value

            api_key = request.query_params.get('api_key')
            # process_api_response = api_key
            # if process_api_response == '504a51bf-c483-4ac5-b2dd-4f209eabcbf8':
            process_api_response = processApikey(api_key)
            if process_api_response.status_code == 200:
                company_id = formdata.get('company_id')
                description = formdata.get('description')
                qrcode_color = formdata.get('qrcode_color')
                logo = formdata.get('logo')

                created_by = formdata.get("created_by")

                host = request.META['HTTP_HOST']

                brand_name = formdata.get("brand_name")
                service = formdata.getlist("service")
                url = formdata.get("url")
                country = formdata.get("country")
                
                
                
                
                if country:
                    country = country.replace('-', ' ')
                region = formdata.get("region")
                
                
                if service:
                    service = service.replace('-', ' ')
                service = formdata.get("service")
                
                if region:
                    region = region.replace('-', ' ')
                promotional_sentence = formdata.get("promotional_sentence")
                username = formdata.get("username")
                name = formdata.get("name")
                email = formdata.get("email")
                link = formdata.get('link')
                participantsLimit = formdata("participantsLimit")

                formdata["start_date"] = my_date(myDict["start_date"])
                formdata["end_date"] = my_date(myDict["end_date"])

                print('form data printier', formdata)

                serializer = UpdateQrCodeSerializerV2(
                    survey, data=formdata, partial=True)
                if serializer.is_valid():
                    res = serializer.save()
                    res_data = serializer.data
                    update_to_remote_db(res_data)

                    logo = res_data['logo']
                    company_id = company_id
                    created_by = created_by
                    qrcode_color = qrcode_color
                    description = description

                    payloads = {
                        "logo": logo,
                        "company_id": company_id,
                        "description": description,
                        "created_by": created_by,
                        "qrcode_color": qrcode_color,
                    }
                    payload = {key: value for key,
                               value in payloads.items() if value is not None}
                    qrcode_url = f'https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_id}/?api_key=' + api_key
                    payload
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
