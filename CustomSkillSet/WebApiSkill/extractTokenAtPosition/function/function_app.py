import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#The incoming request from AI Search WebApi will be in the following format: https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api#sample-input-json-structure
#The response from the function should be in the following format: https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api#sample-output-json-structure
@app.route(route="extractTokenAtPosition")
def extractTokenAtPosition(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP extractTokenAtPosition function processed a request.')
    try:
        logging.info(f"Received RAW Body: {req.get_body()}")
        body = json.dumps(req.get_json())

        if body:
            result = compose_response(body)

            return func.HttpResponse(result, mimetype="application/json")
        else:
            return func.HttpResponse(
                "Invalid body",
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            "Invalid body",
            status_code=400
        )

def compose_response(json_data):
    values = json.loads(json_data)['values']

    # Prepare the Output before the loop
    results = {}
    results["values"] = []

    for value in values:
        output_record = splitString(data=value['data'], recordId=value['recordId'])
        results['values'].append(output_record)

    logging.info(f"HTTP Return: {results}")
    return json.dumps(results, ensure_ascii=False)

def splitString(data, recordId):
    # Custom Web API skill JSON reference
    # https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api

    output_record = {
        "recordId": None,
        "data": {},
        "errors": None,
        "warnings": None
    }

    try:
        logging.info(f"Data in values array: {data}")
        text = data['text']
        delimiter = data['delimiter']
        position = data['position']

        textSplit = text.split(delimiter)[int(position)]

        output_record['recordId'] = recordId
        output_record['data']['text'] = textSplit

    except IndexError as error:
        logging.error(f"Invalid text, delimiter to split. Error: {error}")
        output_record['recordId'] = recordId
        output_record['errors'] = [{"message": "Invalid text, delimiter to split. Error: " + str(error)}]

    except Exception as error:
        logging.error(f"Error: {error}")
        output_record['recordId'] = recordId
        output_record['errors'] = [{"message": "Error: " + str(error)}]

    logging.info(f"output_record: {output_record}")
    return output_record

