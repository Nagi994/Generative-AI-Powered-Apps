#!/usr/bin/env python3

# Import necessary libraries
import torch  # PyTorch for deep learning operations
from ibm_watson_machine_learning.foundation_models import Model  # IBM Watson Machine Learning SDK for model interaction
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM  # LangChain extension for IBM Watson models
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams  # Parameter names for text generation


# Credentials for accessing the IBM Watson Machine Learning service
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",  # URL for the IBM Watson Machine Learning service endpoint
    "apikey": "YOUR_API_KEY"  # Replace with your actual API key from IBM Cloud
}

# Parameters for controlling text generation
params = {
    GenParams.MAX_NEW_TOKENS: 800,    # Maximum number of tokens the model can generate
    GenParams.TEMPERATURE: 0.1        # Controls randomness of text generation (lower is more deterministic)
}

# Load the Llama 2 70B chat model from IBM Watson Machine Learning
LLAMA2_model = Model(
    model_id='meta-llama/llama-2-70b-chat',  # Model ID on IBM Watson Machine Learning
    credentials=my_credentials,             # Credentials for authentication
    params=params,                           # Generation parameters
    project_id="skills-network"              # Your project ID on IBM Watson Machine Learning (if applicable)
)

# Create an instance of the WatsonxLLM interface for interacting with the model using LangChain
llm = WatsonxLLM(LLAMA2_model)

# Send a prompt to the model and print the generated response
response = llm("How to read a book effectively?")  # Ask the model a question
print(response)  