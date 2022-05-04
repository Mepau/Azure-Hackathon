import logging
from types import SimpleNamespace
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


def main(req: func.HttpRequest,
        slObjects: func.DocumentList) -> func.HttpResponse:
         
    logging.info('Python HTTP trigger function processed a request.')

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    
    req_body= req.get_json()
    words= req_body.get("words")

    new_req_body = str.encode(json.dumps(words))

    #Define url with the same given from Machine learning endpoint container.
    url = 'http://66e27235-8a38-4433-b58b-33942b5ee9de.australiaeast.azurecontainer.io/score'
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    new_req = urllib.request.Request(url, new_req_body, headers)

    try:
        #Ideally this would be done by using durable functions orchestrations and binding the db with query string passed by this starting function
        jsonDocuments = [(lambda document: json.loads(document.to_json(), object_hook=lambda d: SimpleNamespace(**d)))(document) for document in slObjects]
        logging.info(jsonDocuments)
        response = urllib.request.urlopen(new_req)
        result = response.read()  
        guesses = literal_eval(result.decode())

        

        if guesses:
            #for guess in guesses:
            #    if guess
            return func.HttpResponse(f"{guesses}")
        else:
            return func.HttpResponse(
             "No results found by the machine learning algorithm",
             status_code=200
        )
    except urllib.error.HTTPError as error:
        return func.HttpResponse(
             f"There was an error {error}",
             status_code=400
        )

    