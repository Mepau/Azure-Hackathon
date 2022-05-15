# Speech to Sign Azure application

This filepath contains the scripts for the different ***AI trainers, testing, models, entryscripts and env.yml*** needed for creation and deployment to **Azure Machine Learning** service.

For local testing ensure to install all the modules required in the **requirements.txt** with `pip install -r requirements.txt`

*Sign Language Translator* entryscript requires 3 dependencies to run in container when model is deployed.
1. **AttnDecoderRNN.py**
2. **EncoderRNN.py**
3. **spanish-sign.txt** found in `./data/` filepath

