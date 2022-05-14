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
    sentence= req_body.get("sentence")

    new_req_body = str.encode(sentence)

    #Define url with the same given from Machine learning endpoint container.
    url = 'http://55b5dae8-40d6-4139-a4ec-d24549fb6050.australiaeast.azurecontainer.io/score'
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    new_req = urllib.request.Request(url, new_req_body, headers)

    try:
        #Ideally this would be done by using durable functions orchestrations and binding the db with query string passed by this starting function
        jsonDocuments = [(lambda document: json.loads(document.to_json(), object_hook=lambda d: SimpleNamespace(**d)))(document) for document in slObjects]
  
        response = urllib.request.urlopen(new_req)
        result = response.read()
        logging.info(result.decode())
        guesses = literal_eval(result.decode())
        logging.info(guesses)

        result= []
        if guesses:
            #Ideally this shouldn't be done in function but rather use CosmosDB SDK for fast and low latency queries
            #Another design would be using azure durable for orchestration with input binding to the activity function with query being guesses containing tagId
            for guess in guesses:
                for document in jsonDocuments:
                    if document.id == guess:
                        result.append(document.url)
            return func.HttpResponse(f"{result}")
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

    