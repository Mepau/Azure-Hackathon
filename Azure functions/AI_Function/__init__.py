import logging
import azure.functions as func
import urllib.request
import json
import os
import ssl
from ast import literal_eval

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    
    req_body= req.get_json()
    words= req_body.get("words")

    new_req_body = str.encode(json.dumps(words))

    url = 'http://bae7d975-f237-4d81-9bd5-75a845165442.australiaeast.azurecontainer.io/score'
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    new_req = urllib.request.Request(url, new_req_body, headers)

    try:
        response = urllib.request.urlopen(new_req)
        result = response.read()  
        words_res = literal_eval(result.decode())


        if words_res:
            return func.HttpResponse(f"{words_res}")
        else:
            return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    except urllib.error.HTTPError as error:
        return func.HttpResponse(
             f"There was an error {error}",
             status_code=400
        )

    
