#Speech to Sign Azure application

This application was made for **Latin American Azure Hackathon + AI Challenge**.

This application is for translating speech in spanish to a visual representation (in this case short videos) of sign language equivalent sentence.

This is done by:

1. Hosting a React application with **Azure App Services**
2. Recognizing speech with **Azure Speech Services**
    - This is done by using **CognitiveServices Speech SDK**
3. Translating spanish sentences with a custom Encoder-Decoder Neural network to sign expressions
    - The AI model was written with *python* and *PyTorch*
    - Trained firstly using **Machine Learning Studios workspace**(To try it out!) then locally on own machine
    - Uploaded model to **Machine Learning Studios workspace**
    - Deployed model with an entryscript on a web endpoint for real time inferencing
4. Serverless application using **Azure Functions** for retrieving key for speech services and both hiding and providing access to model endpoint.
5. Storing objects containing video URLS with **Azure Cosmos DB**
    - Used as input binding to AI Function

