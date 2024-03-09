from django.shortcuts import render
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from decouple import config
# Create your views here.
##Used to track messages
common_api_key = config("COMMON_API_KEY")
error_message = ""
## T
class CustomError(Exception):
    pass
def get_data(api_key, fil = False, payment=False ):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    data = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowell_survey",
                        "coll_name":"survey_search_data",
                        "payment":payment
                        }
    if fil:
        data[ "filters"]=json.dumps(fil)

    wanted_dets = list()

    content_length = len(json.dumps(data))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(data))}
    r=requests.get(url,data=data)
    print("data ------------->",data)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)['data']
        res_data = {"data":raw_data, "success":True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->",raw_data)
    else:
        res_data = {"success":False, "status_code":r.status_code, "text":json.loads(r.text)['message']}
    return res_data
def insert_data(api_key,data, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    payload = {
                        "api_key":api_key,
                        "operation":"insert",
                        "db_name":"dowell_survey",
                        "coll_name":"survey_search_data",
                        "data":data,
                        "payment": payment
                        }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(payload))}
    r=requests.post(url,json=payload)
    print("data ------------->",payload)
    # print("response.status------------->",response.status)
    print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)
        res_data = {"status_code":r.status_code, "text":raw_data['message'],"search_result_id":raw_data['data']['inserted_id'], "success":True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->",raw_data)
    else:
        raw_data =  json.loads(r.text)
        res_data = {"success":False, "status_code":r.status_code, "text":raw_data['message']}
    return res_data

def update_data(api_key,id,data, replace_group_list = False,  payment=False ):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    concat_data = data
    if "group_list" in data and not replace_group_list:
        print("group_list was there")
        old_data = get_data(api_key, fil={"_id":id})
        print("old_data ==> ", old_data)
        concat_data['group_list'] = list(set(old_data['data'][0]["group_list"] +data['group_list']))
        # print("concat_data ==> ", concat_data)
    print("concat_data ==> ", concat_data)
    payload = {
                        "api_key":api_key,
                        "operation":"update",
                        "db_name":"dowell_survey",
                        "coll_name":"survey_search_data",
                        "query": {"_id": id },
					    "update_data": concat_data,
					    "payment":payment
                        }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(payload))}
    r=requests.put(url,json=payload)
    print("data ------------->",payload)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)
        res_data = {"status_code":r.status_code, "text":raw_data['message'], "success":True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->",raw_data)
    else:
        raw_data =  json.loads(r.text)
        res_data = {"success":False, "status_code":r.status_code, "text":raw_data['message']}
    return res_data
def delete_data(api_key,fil , payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
                        "api_key":api_key,
                        "operation":"delete",
                        "db_name":"dowell_survey",
                        "coll_name":"survey_search_data",
                        "query": fil,
                        "payment":payment
                        }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(payload))}
    r=requests.delete(url,json=payload)
    print("data ------------->",payload)
    print("response.status------------->",r.status_code)
    print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200 or r.status_code == 405:
        raw_data =  json.loads(r.text)
        res_data = {"status_code":r.status_code, "text":raw_data['message'], "success":True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->",raw_data)
    else:
        raw_data =  json.loads(r.text)
        res_data = {"success":False, "status_code":r.status_code, "text":raw_data['message']}
    return res_data

def snyc_groups(username, api_key):
    recs = get_data(api_key,{"username":username})
    recover_list = []
    for h in recs['data']:
        if h['doc_type'] == "master":
            recover_list = h['recover_list']
    old_list = [list(i.keys()) for i in recover_list]
    temp_res = {}
    for t in recs['data']:
        if t['group_name'] in old_list:
            temp_res = update_data(api_key, t['_id'], {'group_name': recover_list[t['group_name']]})
            if not temp_res['success']:
                error_message = "Kindly start the synchronization again."
                res_data = {"success":False, "status_code":temp_res.status_code, "text":error_message}
                return res_data
    return {"status_code":temp_res.status_code, "text":"Synchronization successfully done!", "success":True}



class GetSurveysSearchData(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"message":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            wanted_dets = list()
            payload = {
                    "api_key":api_key,
                    "operation":"fetch",
                    "db_name":"dowell_survey",
                    "coll_name":"survey_search_data",
                }
            myDict = request.data
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']

            if "filters" in myDict:
                res = get_data(api_key, myDict['filters'], payment)
            else:
                res = get_data(api_key, payment)
            if res['success']:
                wanted_dets = res['data']
            else:
                error_message = res['text']
                raise CustomError(res['text'])
            # wanted_dets.extend(get_data(payload))
            res = {"data": wanted_dets}
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class CreateSurveysSearch(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"message":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = common_api_key
            # api_key=""
            myDict = request.data
            # username = myDict['em']
            payment =  False
            if "email" in myDict:
                email = myDict['email']
            else:
                error_message = "email is missing from payload!"
                raise CustomError(error_message)
            if "place_name" in myDict:
                place_name = myDict['place_name']
            else:
                error_message = "place_name is missing from payload!"
                raise CustomError(error_message)
            if "address" in myDict:
                address = myDict['address']
            else:
                error_message = "place_name is missing from payload!"
                raise CustomError(error_message)
            if "mobile_no" in myDict:
                mobile_no = myDict['mobile_no']
            else:
                error_message = "mobile_no is missing from payload!"
                raise CustomError(error_message)    
            if "region" in myDict:
                region = myDict['region']
            else:
                error_message = "region is missing from payload!"
                raise CustomError(error_message)
            if "webaddress" in myDict:
                webaddress = myDict['webaddress']
            else:
                error_message = "webaddress is missing from payload!"
                raise CustomError(error_message)
            
            res = {}
            data = {
            "email":email,
            "place_name":place_name,
            "address":address,
            "mobile_no":mobile_no,
            "region":region,
            "webaddress":webaddress
                }

            res = insert_data(api_key,data)
            
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)

class UpdateSearchData(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"message":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            # username = myDict['username']
            if "new_survey_detail" in myDict :
                new_survey_details = myDict['new_survey_detail']
                print("type ===",type(new_survey_details))
                if not isinstance(new_survey_details, dict):
                    error_message = "Check the new_survey_detail if json!"
                    # r = json.dumps(error_message)
                    raise CustomError(error_message)
                # return Response(r, status=status.HTTP_400_BAD_REQUEST)

            else:
                error_message = "Check the new_survey_detail if present!"
                raise CustomError(error_message)

            
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            id = myDict['search_result_id']
            check_res = get_data(api_key,{"_id":id}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "Search data does not exist!"
                raise CustomError(error_message)

            else:
                temp_data = check_res["data"][0]
                res = update_data(api_key,temp_data["_id"],new_survey_details, payment )
                if not res['success']:
                    error_message = res['text']
                    raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class DeleteSearchData(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"message":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            if "search_result_id" in myDict:
                search_result_id = myDict['search_result_id']
                res = delete_data(api_key, {"_id":search_result_id}, payment)
            else:
                error_message = "Search data does not exist!"
                raise CustomError(error_message)

            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)
