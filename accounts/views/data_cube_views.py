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



class GetSurveys(APIView):
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


class CreateUserProfile(APIView):
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
            username = myDict['username']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(api_key,{"username":username,"doc_type":"master"}, payment)
            res = {}
            if len(check_res['data']) == 0:
                data = {
                    "username": username,
                    "doc_type":"master",
                    "group_list":[],
                    "recover_list":[],
                }

                res = insert_data(api_key,data)
            else:
                error_message = "User exists already!"
                raise CustomError(error_message)
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class CreateLocGroup(APIView):
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
            username = myDict['username']
            group_name = myDict['group_name']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(api_key,{"username":username,"doc_type":"master"}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "User does not exist!"
                raise CustomError(error_message)

            else:
                id = check_res['data'][0]['_id']
                data = {
                    "group_list":[group_name]
                }
                update_res = update_data(api_key,id,data , payment)
                if update_res['success']:
                    res = update_res
                else:
                    error_message = update_res['text']
                    raise CustomError(error_message)
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)
class CreateLocation(APIView):
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
            username = myDict['username']
            group_name = myDict['group_name']
            loc_detail = myDict['loc_detail']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(api_key,{"username":username,"doc_type":"master"}, payment)
            res = {}
            if not check_res['success']:
                error_message = check_res['text']
                raise CustomError(error_message)
            if 'data' in check_res and len(check_res['data']) == 0:
                error_message = "User does not exist!"
                raise CustomError(error_message)

            else:
                data = {
                        "username": username,
                        "doc_type":"slave",
                        "group_name":group_name,
                        "loc_details":loc_detail
                        }

                res = insert_data(api_key,data, payment )
                if not res['success']:
                    error_message = res['text']
                    raise CustomError(error_message)
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)

class UpdateLocGroup(APIView):
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
            username = myDict['username']
            old_name = myDict['old_group_name']
            new_group_name = myDict['new_group_name']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(api_key,{"username":username}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "User does not exist!"
                raise CustomError(error_message)

            else:
                for i in check_res["data"]:
                    res = {}
                    if i['doc_type'] == "master":
                        if 'recover_list' not in i:
                            i['recover_list'] =[]
                        for j in range(len(i['group_list'])):
                            if i['group_list'][j] == old_name:
                                i['recover_list'].append({old_name:new_group_name})
                                i['group_list'][j]  = new_group_name
                                break
                        res = update_data(api_key,i["_id"],{"group_list":i['group_list'],
                                                                 "recover_list":i['recover_list'],},True, payment )
                    else:
                        res = update_data(api_key,i["_id"],{"group_name":new_group_name}, payment )
                    if not res['success']:
                        error_message = res['text']
                        raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)

class UpdateLocation(APIView):
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
            new_loc_details = myDict['new_loc_detail']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            id = myDict['loc_id']
            check_res = get_data(api_key,{"_id":id}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "Location does not exist!"
                raise CustomError(error_message)

            else:
                temp_data = check_res["data"][0]
                temp_data['loc_details'] = new_loc_details
                res = update_data(api_key,temp_data["_id"],{"loc_details":new_loc_details}, payment )
                if not res['success']:
                    error_message = res['text']
                    raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class DeleteUserProfile(APIView):
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
            username = myDict['username']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            res = delete_data(api_key, {"username":username}, payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)
class DeleteLocGroup(APIView):
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
            username = myDict['username']
            group_name = myDict['group_name']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_user = get_data(api_key, {"username":username, "doc_type":"master"}, payment)

            if not check_user["success"]:
                error_message = check_user['text']
                raise CustomError(error_message)
            culprit_list = check_user['data'][0]['group_list']
            if group_name in culprit_list:
                culprit_list.remove(group_name)
            update_res = update_data(api_key, check_user['data'][0]['_id'],{"group_list":culprit_list}, True, payment)
            if not update_res["success"]:
                error_message = update_res['text']
                raise CustomError(error_message)
            res = delete_data(api_key, {"username":username, "group_name":group_name}, payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class DeleteLocation(APIView):
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
            id = myDict['id']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            res = delete_data(api_key,{"_id":id}, payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)



class SyncGroups(APIView):
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
            username = myDict['username']
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = snyc_groups(username, api_key, payment)
            res = {}
            if check_res['success']:
                res = check_res
            else:
                error_message = check_res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)




# api_key = "783ae055-6844-4a73-8be7-20b6a157ab9c"

# get_data(api_key)