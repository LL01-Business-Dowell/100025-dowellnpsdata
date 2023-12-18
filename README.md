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

For detailed examples and testing the API endpoints, you can find the Postman documentation [here](https://documenter.getpostman.com/view/25619963/2s9YBxZbzG).
