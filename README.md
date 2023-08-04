# DoWell Surveys
## Illustration
This API is used to provide a platform for a survey that has its form hosted in another server. A QR code is created
which when scanned displays the form. The users can continue to fill in the survey. This QR code can be printed and then stuck 
on walls or tables where it can be accessed by the end users. 

While creating the API one is required to set a start and an end date. If an end-user should try to scan before the survey 
starts or after it ends then they will get feedback to say the same otherwise the form will be there to fill.
<div>



### step 1
<div>First we click "create my own survey button" </div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206561/sbs-email-template/dowell/Feedback_lnmbtk.jpg' height='300' width='200'/>

### step 2
<div>We get to fill in the form where we start by uploading an image for the logo then continue with the brand name of the product being surveyd, enter the url of the hosted form, countries, and regions where this 
survey should take part, then a promotional sentence at the bottom. Then click create a survey.</div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/Create_servey_qhp4cw.jpg' height='300' width='200'/>


### step 3
<div>The QR code is then created and displayed. After clicking the privacy policy button we set the survey timeline </div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206561/sbs-email-template/dowell/Create_QR_code_juazmx.jpg' height='300' width='200'/>


### step 4
<div>At this stage, we set the start and end dates</div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/survey_date_1_ucdb4x.jpg' height='300' width='200'/>


### step 5
<div>Feedback is given on the success or failure
</div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/survey_date_1_1_iutxdq.jpg' height='300' width='200'/>


### step 6
<div>The creator details are collected here. The email filled in here will receive the details about the survey created/
</div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/Create_QR_code_1_vp75ut.jpg' height='300' width='200'/>

### step 7
<div> The feedback on success or failure is given.</div>
<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/survey_date_1_1_iutxdq.jpg' height='300' width='200'/>

### step 8
<div>The form to be displayed to the user is shown.</div> 

<img src='https://res.cloudinary.com/dhmvn4nnf/image/upload/v1667206560/sbs-email-template/dowell/iframe_ngbgwz.jpg' height='300' width='200'/>

</div>




<!-- ======================The API Documentation============================== -->


# DoWell Surveys API Documentation

## Introduction
This API documentation provides details on how to use the endpoints for creating and updating Dowell Surveys.

## API Endpoints

### Create or Update Dowell Survey

- **URL**: `/get-survey/?api_key=YOUR_API_KEY`
- **Methods**: POST (Create), PUT (Update)

The `POST` method is used to create a new Dowell Survey, and the `PUT` method is used to update an existing survey. You need to include the `api_key` parameter in the URL with your valid API key.


#### Request Parameters

| Parameter             | Type     | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| api_key               | string   | The API key required to access the service.     |
| company_id            | integer  | The ID of the company associated with the survey.|
| logo                  | file     | The logo image file for the survey.             |
| brand_name            | string   | The brand name for the survey.                  |
| service               | string   | The service.                 |
| url                   | string   | The url of the survey document.                 |
| country               | string   | The country where the survey should be done.                 |
| region                | string   | The region in the selected country where the survey should be done.                 |
| promotional_sentence  | string   | Input any promotional message for the survey.                 |
| username              | string   | The username                 |
| name                  | string   | The name                 |
| email                  | string   | The email                 |
| start_date                  | string   | The date the survey should tart                 |
| end_date                  | string   | The The date the survey should end                 |
                                            |

#### Responses

- **200 OK**: Request successful.
- **201 Created**: The survey was successfully created.
- **400 Bad Request**: The request data is invalid or missing required parameters.
- **404 Not Found**: The requested survey was not found (for PUT method).

## Postman Documentation

For detailed examples and testing the API endpoints, you can find the Postman documentation [here](https://www.postman.com/telecoms-meteorologist-97889107/workspace/33939f3e-5474-469e-903e-6b5438341be9/share?collection=24456149-3b37fa2b-3430-4691-b6db-1273a7c1562d&target=embed).
