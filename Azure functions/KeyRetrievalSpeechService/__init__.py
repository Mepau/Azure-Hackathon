import logging
import azure.functions as func
import urllib.request
import json
import os
import ssl

def main(req: func.HttpRequest) -> func.HttpResponse:

    #new_req_body = str.encode(json.dumps(words))

    #Replace with the susbcription key for the Azure Speech Service
    speechKey = ""

    #Replace with the region of said Azure Speech Service
    speechRegion = ""

    headers = { "Ocp-Apim-Subscription-Key": speechKey, "Content-Type": "application/json"}

    url = f"https://{speechRegion}.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

    new_req = urllib.request.Request(url, {} ,headers)

    try:
        
        response = urllib.request.urlopen(new_req)
        result = response.read()
        return func.HttpResponse(json.dumps({ "token": result.decode(), "region": speechRegion }))
        
    except urllib.error.HTTPError as error:
        logging.info("The request failed with status code: " + str(error.code))

       # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        logging.info(error.info())
        logging.info(error.read().decode("utf8", 'ignore'))