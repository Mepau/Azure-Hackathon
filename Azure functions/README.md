# Speech to Sign Azure application

To test locally first install a venv in this filepath as root then `python -m venv .venv`

Also for locally test or deployment need to:

1. In *KeyRetrievalSpeechService/\_\_init\_\_.py* replace:
    - `speechKey` value to one obtained from your **Azure Speech Service**
    - `speechRegion` value to the one from which region you created said service.
2. In *AIFunction/\_\_init\_\_.py* replace:
    - `url` value to the endpoint obtained from deployment of the model in **Azure Machine Learning Service**
