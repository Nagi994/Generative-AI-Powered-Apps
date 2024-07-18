#!/usr/bin/env python3
# Shebang: Specifies the interpreter (Python 3) for the script.

# Imports
from ibm_watson_machine_learning.foundation_models import Model  # For loading and interacting with the Watsonx model.
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes  # For specifying the model type.
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods  # For setting the decoding method.
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams  # For defining generation parameters.

import requests  # For making HTTP requests to the Watson APIs.


# Placeholder for Credentials - Replace with your actual values!
Watsonx_API = "Your WatsonX API Key"
Project_id = "Your Project ID"


# Authentication and Configuration
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",  # URL for the IBM Watson Machine Learning service.
    "apikey": Watsonx_API  # API key for accessing the Watsonx service.
}

project_id = Project_id    # Project ID (replace with your project ID if needed).

# Choose Model
model_id = ModelTypes.FLAN_UL2  # Select the FLAN-UL2 model from the available options.
# You could choose other models like 'google/flan-t5-xxl' based on your needs.

# Generation Parameters
parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,   # Greedy decoding for faster, less flexible generation.
    GenParams.MIN_NEW_TOKENS: 1,                       # Minimum new tokens to generate.
    GenParams.MAX_NEW_TOKENS: 1024                     # Maximum number of tokens to generate.
}

# Initialize the Model
model = Model(
    model_id=model_id,       # The chosen model ID.
    params=parameters,       # Generation parameters.
    credentials=credentials,  # Authentication credentials.
    project_id=project_id     # Project ID if applicable.
)




### Watson Speech and Translation Functions ###

def speech_to_text(audio_binary):
    """
    Converts speech (audio data) into text using the Watson Speech-to-Text service.

    Args:
        audio_binary (bytes): The audio data in binary format.

    Returns:
        str: The transcribed text.
    """

    base_url = "..."  # Replace with the actual base URL of your Watson Speech-to-Text service.
    api_url = f"{base_url}/speech-to-text/api/v1/recognize"

    params = {
        'model': 'en-US_Multimedia'  # Model to use for transcription (English US Multimedia).
    }

    response = requests.post(api_url, params=params, data=audio_binary).json()

    text = 'null'  # Default value in case transcription fails.
    if response.get('results'):  
        print('Speech-to-Text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')  # Extract transcript.
        print('recognised text: ', text)
    return text

def text_to_speech(text, voice=""):
    """
    Converts text into speech (audio data) using the Watson Text-to-Speech service.

    Args:
        text (str): The text to be converted into speech.
        voice (str, optional): The voice to use for synthesis (e.g., "en-US_AllisonV3Voice"). Defaults to "".

    Returns:
        bytes: The synthesized audio data in WAV format.
    """
    # Set up Watson Text-to-Speech HTTP Api url
    base_url = '...'  # Replace with the actual base URL of your Watson Speech-to-Text service.
    api_url = f"{base_url}/text-to-speech/api/v1/synthesize?output=output_text.wav"
    # Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    
    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }

    # Send a HTTP Post reqeust to Watson Text-to-Speech Service
    response = requests.post(api_url, headers=headers, json=json_data)
    return response.content


### Watsonx LLM Function ###
def watsonx_process_message(user_message):
    """
    Processes a user message by prompting the Watsonx LLM to translate it from English to Spanish.

    Args:
        user_message (str): The message in English to be translated.

    Returns:
        str: The translated message in Spanish.
    """

    # Format the Prompt
    prompt = f"""You are an assistant helping translate sentences from English into Spanish.
    Translate the query to Spanish: `{user_message}`."""

    # Call the Model
    response_text = model.generate_text(prompt=prompt)  # Get the model's response.
    print("Watsonx response:", response_text)           # Print the response (optional for debugging).
    return response_text

