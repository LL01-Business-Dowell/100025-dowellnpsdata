from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from datetime import datetime, date
from accounts.views.helper import upload_to_remote_db, update_to_remote_db
from api.serializers import *
from api.models import QrCode, QrCodeV2, SurveyCoordinator
from django.shortcuts import get_object_or_404
import ast
from django.conf import settings
import ast


import requests
from urllib.parse import urlparse, parse_qs


class CustomError(Exception):
    pass


def my_date(date_str):

    date_object = datetime.strptime(date_str, '%d-%m-%Y').date()

    return date_object


def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    # print('url for checking api_key', url)
    payload = {
        "service_id": "DOWELL10016"
    }

    response = requests.post(url, json=payload)
    # print(f"This is the response text {response.text}")
    # print("Response Status Code:", response.status_code)
    return response


class GetDowellSurvey(APIView):
    def get(self, request, format=None):
        return JsonResponse({"data": "Kindly use a POST request instead of GET"})

    def post(self, request, format=None):

        current_date = datetime.now()
        dates = current_date.date()
        myDict = request.data
        # print("mydict ===> ", myDict)
        # p_list = myDict['p_list']
        # print('This is data request ', myDict)
        formdata = {}
        files = {}

        required_fields = ['qrcode_type', 'quantity' ,'company_id', 'logo', 'brand_name', 'service', 'url',
                           'country', 'region', 'promotional_sentence', 'username',
                           'name', 'email', 'participantsLimit', 'link',  'description', 'created_by', 'search_result_id']

        missing_fields = [field for field in required_fields if field not in myDict]
        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            return Response({"error": f"The following fields are missing in the request data: {missing_fields_str}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            api_key = request.query_params.get('api_key')
            # process_api_response = api_key
            # if process_api_response == '76092219-c570-4c86-88f0-efa63966e06b':
            process_api_response = processApikey(api_key)
            if process_api_response.status_code == 200:
                company_id = myDict['company_id']
                formdata['logo'] = myDict['logo']
                formdata["brand_name"] = myDict["brand_name"]
                # formdata["service"] = myDict.getlist("service")
                formdata["service"] = myDict["service"]
                formdata["url"] = myDict["url"]
                formdata["country"] = myDict.getlist("country")
                formdata["region"] = myDict.getlist("region")
                # formdata["country"] = myDict["country"]
                # formdata["region"] = myDict["region"]
                formdata["promotional_sentence"] = myDict["promotional_sentence"]
                formdata["username"] = myDict["username"]
                formdata["name"] = myDict["name"]
                formdata["email"] = myDict["email"]
                formdata["participantsLimit"] = myDict["participantsLimit"]
                formdata["link"] = myDict["link"]
                # formdata["start_date"] = my_date(myDict["start_date"])
                # formdata["end_date"] = my_date(myDict["end_date"])
                formdata["longitude"] = myDict["longitude"]
                formdata["latitude"] = myDict["latitude"]
                formdata['category'] = myDict["category"]
                formdata['search_result_id'] = myDict["search_result_id"]
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
                print('country type ', type(myDict.getlist("country")))
                serializer = CreateQrCodeSerializerV2(data=formdata)
                if serializer.is_valid():
                    print('True')
                    res = serializer.save()
                    res_data = serializer.data
                    # print('This is the res data ', res_data)
                    # upload_to_remote_db(res_data)


                    '''================================='''
# 070271185547


                    context = {
                        'qrcode': res_data['qr_code'],
                        # 'link': 'https://'+settings.HOSTNAME+'/iframe?survey_id=' + str(res_data['id']),
                        'link':myDict["link"]+"?survey_id=" + str(res_data['id'])

                    }
                    qrcode_type = "Link"
                    quantity = 1
                    company_id = company_id
                    search_result_id = myDict.get('search_result_id')
                    print('search_result_id ', search_result_id)
                    # link = 'https://'+settings.HOSTNAME + \
                    #     '/iframe?survey_id=' + str(res_data['id'])
                    link= myDict["link"]+"?survey_id=" + str(res_data['id'])
                    description = res_data['promotional_sentence']
                    created_by = res_data['username']
                    logo = res_data['logo']
                    survey_id = res_data['id']

                    qrcode_url = 'https://www.qrcodereviews.uxlivinglab.online/api/v2/qr-code/?api_key=' + api_key
                    payload = {
                        "qrcode_type": qrcode_type,
                        "quantity": quantity,
                        "company_id": company_id,
                        "logo":logo,
                        "link": link,
                        "description": description,
                        "created_by": created_by,
                        "search_result_id": search_result_id
                    }
                    headers = {"Content-Type": "multipart/form-data"}

                    res = requests.post(qrcode_url, data=payload)
                    # res = {"qr_code_generator_response": res}

                    res_obj = json.loads(res.text)
                    keys_to_add = ['id','country', 'region', 'name','email', 'username', 'promotional_sentence' ,'participantsLimit', 'category', 'latitude', 'longitude', 'search_result_id']
                    for qrcode in res_obj['qrcodes']:
                        # qrcode.update(res_data)
                        qrcode.update({key: res_data[key] for key in keys_to_add if key in res_data})

                    surve = QrCodeV2.objects.get(id=survey_id)
                    formdata = {}
                    data = res_obj
                    print('Survey  res_obj  ',  survey_id)
                    qrcode_id = data['qrcodes'][0]['qrcode_id']
                    formdata["qr_code_id"] = qrcode_id
                    print("QR Code ID:", formdata)
                    serialize = UpdateQrCodeSerializerV2(surve, data=formdata, partial=True)
                    if serialize.is_valid():
                        res = serialize.save()
                        # res = serializer.save()
                        res_dat = serialize.data
                        # print('Ree ', res_dat)
                    '''============================================='''

                    return Response(res_obj, status=status.HTTP_200_OK)
                else:
                    return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("API Key validation failed.", status=status.HTTP_400_BAD_REQUEST)

            # res = requests.get(url, data=formdata, files=files)

        except CustomError:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)





    def put(self, request, format=None):
        myDict = request.data
        # p_list = myDict['p_list']



        formdata = {}
        files = {}

        try:
            try:
                qrcode_survey_id = myDict['qrcode_id']
                Survey_id = myDict['id']
                print('Qrcode_survey ', qrcode_survey_id)
                # responses = requests.get(
                #     f"https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_survey_id}/")
                # print('Response ', responses)
                # response_json = responses.json()
                # print('Response_json ', response_json)
                # links = response_json["response"][0]["link"]
                # parsed_url = urlparse(links)
                # query_params = parse_qs(parsed_url.query)
                # survey_id = query_params.get("survey_id")[
                #     0] if "survey_id" in query_params else None
                survey_id = Survey_id

                survey = QrCodeV2.objects.get(id=survey_id)
            except QrCodeV2.DoesNotExist:
                raise Http404("Survey not found")

            for key, value in myDict.items():
                if value:  # Check if the value is not empty
                    formdata[key] = value

            api_key = request.query_params.get('api_key')
            process_api_response = api_key
            # if process_api_response == '504a51bf-c483-4ac5-b2dd-4f209eabcbf8':
            process_api_response = processApikey(api_key)
            if process_api_response.status_code == 200:
                company_id = formdata.get('company_id')
                
                description = formdata.get('description')
                print('This is my Description ', description)
                qrcode_color = formdata.get('qrcode_color')
                logo = formdata.get('logo')

                created_by = formdata.get("created_by")

                host = request.META['HTTP_HOST']
                brand_name = formdata.get("brand_name")
                service = formdata.get("service")
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
                
                participantsLimit = formdata.get("participantsLimit")

                    # formdata["start_date"] = my_date(myDict["start_date"])
                    # formdata["end_date"] = my_date(myDict["end_date"])


                start_date = formdata.get("start_date")
                if start_date:
                    formdata["start_date"] = my_date(start_date)

                end_date = formdata.get("end_date")
                if end_date:
                    formdata["end_date"] = my_date(end_date)



                print('form ', formdata)
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
                    qrcode_url = f'https://www.qrcodereviews.uxlivinglab.online/api/v2/update-qr-code/{qrcode_survey_id}/?api_key=' + api_key
                    payload
                    headers = {"Content-Type": "multipart/form-data"}
                    res = requests.put(qrcode_url, data=payload)
                    res_obj = json.loads(res.text)
                    
                    keys_to_add = ['id','country', 'region', 'name','email', 'username', 'promotional_sentence' ,'participantsLimit', 'category', 'latitude', 'longitude', 'search_result_id']
                    for key in keys_to_add:
                        if key in res_data:
                            res_obj[key] = res_data[key]
                    # for qrcode in res_obj['response']:
                    # #     # qrcode.update(res_data)
                    #     qrcode.update({key: res_data[key] for key in keys_to_add if key in res_data})
                        
                    return Response(res_obj, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("API Key validation failed.", status=status.HTTP_400_BAD_REQUEST)
        except CustomError:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your payload ", status=status.HTTP_400_BAD_REQUEST)




class ExtractAndFetchSurvey(APIView):
    def post(self, request, format=None):
        # current_date = datetime.datetime.now()
        current_date = datetime.now()
        dates = current_date.date()

        link = request.data.get("link")
        parsed_url = urlparse(link)

        # Extract the survey_id from the query parameters
        query_params = parse_qs(parsed_url.query)
        survey_id = query_params.get('survey_id', [None])[0]
        region = request.data.get("region")
        print('This is the data region ', region)
        

        parts = link.split("/")
        extractedID = survey_id
        if not link:
            return Response({"message": "Link is required"}, status=status.HTTP_400_BAD_REQUEST)

        last_number = self.extract_table_id(link)

        if extractedID is not None:

            survey = get_object_or_404(QrCodeV2, pk=extractedID)
            qr_code_v2 = get_object_or_404(QrCodeV2, pk=extractedID)
            coordinator = SurveyCoordinator.objects.filter(survey=qr_code_v2).first()
            
            
            regions_list = ast.literal_eval(survey.region)
            if region in regions_list:
                print('True')
            else:
                print('False')
            print('regions search ', ast.literal_eval(survey.region))
            
            if dates < survey.start_date:
                response_data = {
                    "isSuccess": False,
                    "message": "Survey has not yet started",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": survey.participantsLimit,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)

            if dates > survey.end_date:
                response_data = {
                    "isSuccess": False,
                    "message": "Survey has already ended",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": survey.participantsLimit,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            

            if survey.start_date <= dates <= survey.end_date:
                participants_limit_str =  coordinator.survey.participantsLimit
                participants_limit_int = int(participants_limit_str)
                print(' participants_limit_int ',  participants_limit_int )
                print(' participants_limit_str ',  participants_limit_str )
                coordinator_participants = coordinator.participants
                print('Participants limit ' , coordinator_participants.get(region, 0))
                # if coordinator_participants.get(region, 0) >= 1:
                if participants_limit_int >= 1 and 'all' in regions_list:
                    response_data = {
                    "isSuccess": True,
                    "message": "Survey can be conducted",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": coordinator_participants,
                    }}
                    return Response(response_data, status=status.HTTP_200_OK)
                    
                elif participants_limit_int >= 1 and region in regions_list:
                    response_data = {
                    "isSuccess": True,
                    "message": "Survey can be conducted",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": coordinator_participants,
                    }}
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "isSuccess": False,
                    "message": "Survey cannot be conducted",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": survey.participantsLimit,
                    }}
                    return Response(response_data, status=status.HTTP_200_OK)
                response_data = {
                    "message": "Survey fetched successfully",
                    "survey_data": {
                        "region for survey ": survey.brand_name,
                        "participantsLimit": survey.participantsLimit,
                    }
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "isSuccess": False,
                    "message": "Survey cannot be conducted at this time",
                    "survey_data": {
                        "region for survey": region,
                        "participantsLimit": survey.participantsLimit,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
        return Response({"message": "Invalid link ID"}, status=status.HTTP_400_BAD_REQUEST)


    def extract_table_id(self, link_id):
        try:
            # Assuming the ID is passed in the URL
            return int(link_id)
        except ValueError:
            return None



class SurveyCounter(APIView):
    def post(self, request, format=None):
        link = request.data.get("link")
        # link = request.data.get("link")
        region = request.data.get("region")
        # print('This is the region ', region)
        # parts = link.split("/")
        # extractedID = parts[-1]
        parsed_url = urlparse(link)

        # Extract the survey_id from the query parameters
        query_params = parse_qs(parsed_url.query)
        survey_id = query_params.get('survey_id', [None])[0]
        extractedID = survey_id
        if not link:
            return Response({"message": "Link is required"}, status=status.HTTP_400_BAD_REQUEST)

        last_number = self.extract_table_id(link)

        if extractedID is not None:
            survey = get_object_or_404(QrCodeV2, pk=extractedID)
            qr_code_v2 = get_object_or_404(QrCodeV2, pk=extractedID)
            coordinator = SurveyCoordinator.objects.filter(survey=qr_code_v2).first()
            participants_limit = coordinator.participants

            if region in participants_limit:
                region_value = int(participants_limit.get(region, 0))
                if region_value >= 1:
                    coordinator.participants[region] = region_value - 1
                    coordinator.save()
            else:
                print(f"{region} does not exist in the dictionary")
            response_data = {
                "isSuccess": True,
                "message": "Survey counted successfully",
                "survey_data": {
                    "brand_name": survey.brand_name,
                    "participantsLimit": participants_limit,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"message": "Invalid link ID"}, status=status.HTTP_400_BAD_REQUEST)


    def extract_table_id(self, link_id):
        try:
            return int(link_id)
        except ValueError:
            return None




class MySurveyFetch(APIView):
    def get(self, request, format=None):
        data = request.data
        print("data-->", data)
        data2 =request.query_params.get("username")
        print("data2-->", data)
        username = request.query_params.get("username")
        username2 = request.data.get("username")
        print('Username ', username)
        print('Username2 ', username2)

        survey = QrCodeV2.objects.filter(username=username)
        # print('This is survey data ', survey)
        serialize = ListQrCodeSerializer(survey, many = True)

        return Response(serialize.data)
    def post(self, request, format=None):
        data = request.data
       
        if 'username' in data:
            username = data['username']
          
            
            
            survey = QrCodeV2.objects.filter(username=username)
            
           
        if 'survey_id' in data:
            survey_id = data['survey_id']
          

            survey = QrCodeV2.objects.filter(id=survey_id)
            
        serialize = ListQrCodeSerializer(survey, many = True).data
        total_survey = survey.count()
        
        end_true_count = sum(1 for item in serialize if item.get('is_end', False))
        end_false_count = sum(1 for item in serialize if not item.get('is_end', False))

        

        
        
        serialize_with_count =  [{'total_survey': total_survey, "active_survey": end_true_count, "closed_survey":end_false_count }] + serialize
        return Response(serialize_with_count)