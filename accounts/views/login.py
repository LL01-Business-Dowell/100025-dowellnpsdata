import requests
from datetime import datetime
from django.views.generic import View
from django.shortcuts import render


class LoInFunc(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'log_in_func.html')

    def post(self, request, *args, **kwargs):
        print("Login")
        loc = request.POST.get("loc", False)
        os = request.POST.get("os", False)
        brow = request.POST.get("brow", False)
        dev = request.POST.get("dev", False)
        time_d = request.POST.get("time", False)
        # drug_category_name = request.POST.get("drug_category_name", False)
        print("loc")
        print(loc)
        print("os")
        print(os)
        print("brow")
        print(brow)
        print("dev")
        print(dev)
        print("time_d")
        print(time_d)
        dd = datetime.now()
        time = dd.strftime("%d:%m:%Y,%H:%M:%S")
        # url = "https://100003.pythonanywhere.com/event_creation"
        username = "dowellFeedback"
        password = "DOWELL@qrcode2022"
        otp="opt"
        ip="192.168.0.41"
        conn="random"
        #  ["otp","loc",dev,"os","brow","time","ip","conn","username","password"]
        url="https://100014.pythonanywhere.com/api/login/"
        userurl="http://100014.pythonanywhere.com/api/user/"
        payload = {"otp": otp, "loc": loc, "dev": dev,
            "os": os, "brow": brow,"time":time,
            "ip": ip, "conn": conn,"username":username, 
            "password": password
            }

        # r = requests.post(url, json=data)
        # print("=============================Login respomsze======================")
        # print(r.text)
        with requests.Session() as s:
            p=s.post(url, data=payload)
            if "Username" in p.text:
                print("p.text")
                print(p.text)
                return p.text
            else:
                user=s.get(userurl)
                print("user.text")
                print(user.text)
                return user.text
        # return r.text
