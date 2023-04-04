import requests
def mail_sender(to_email, to_name,qr_code_src, data_survey_id,survey_title, user_name ):
    url = 'https://100085.pythonanywhere.com/api/feedback-survey/'

    # pay_load = {
        
    # "toEmail":"ericmbuthia11@gmail.com",
    # "toName":"Eric Mbuthia",
    # "topic":"Feedback Survey",
    # "qr_code_src":"https://100025.pythonanywhere.com/media/company_qrcode/Copy%20of%20How%20to%20build%20an%20innovation%20culture%20within%20the%20organisation.png",
    # "data_survey_id":"12",
    # "survey_title": "Cocala",
    # "user_name": "Eric Mbuthia"

    # }
    pay_load = {
        
    "toEmail":to_email,
    "toName":to_name,
    "topic":"Feedback Survey",
    "qr_code_src":qr_code_src,
    "data_survey_id":data_survey_id,
    "survey_title": survey_title,
    "user_name": user_name

    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=pay_load)
    print(type(response))
    print(response)
    res={}
    if response.status_code == 200:
        print('Success!')
        res = {'status':'success','error':False, 'code':200}
        
    elif response.status_code == 404:
        print('Not Found.')
        res = {'status':'Email Not Found', 'error': True, 'code':404}
    else:
        res = {'status':'Not Successfull', 'error': True, 'code':response.status_code}
    # res = json.loads(response.text)
    print(res)
    # return JsonResponse(res)
# mail_sender()
    return res