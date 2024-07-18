from openai import OpenAI
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)  # Configure logging to INFO level for debugging

# Initialize OpenAI client (ensure your API key is set)
openai_client = OpenAI()  

# Function to transcribe speech from audio data
def speech_to_text(audio_binary):
    """
    Converts audio data to text using the Watson Speech-to-Text service.

    Args:
        audio_binary: Raw audio data (bytes) in a supported format.
    
    Returns:
        str: The transcribed text, or 'null' if transcription fails.
    """
    
    base_url = "https://sn-watson-stt.labs.skills.network"  # Watson STT base URL
    api_url = base_url + '/speech-to-text/api/v1/recognize'  # Specific endpoint

    params = {'model': 'en-US_Multimedia'}  # Parameters for English US model

    try:
        # Send POST request to Watson STT API
        response = requests.post(api_url, params=params, data=audio_binary).json() 
    except requests.exceptions.RequestException as e:
        # Handle network errors or other exceptions
        logging.error(f"Error connecting to speech-to-text service: {e}")
        return "null"  # Return null if transcription fails

    text = 'null'  # Default result

    if 'results' in response:  # Check if transcription results are present
        while bool(response.get('results')):
            logging.info(f"Speech-to-Text response: {response}")  # Log response
            # Extract the most likely transcript
            text = response.get('results').pop().get('alternatives').pop().get('transcript')  
            logging.info(f"Recognized text: {text}")  # Log recognized text
            return text  # Return the recognized text
    else:
        # Log an error if 'results' key is not found
        logging.error("Error: 'results' not found in speech-to-text response.")
        return "null"

# Function to convert text to speech audio
def text_to_speech(text, voice=""):
    """
    Converts text to speech using the Watson Text-to-Speech service.

    Args:
        text (str): The text to convert to speech.
        voice (str, optional): The voice to use (default is the service's default).
    
    Returns:
        bytes: The synthesized speech audio data (WAV format).
    """

    base_url = "https://sn-watson-tts.labs.skills.network" 
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    # Append voice parameter if provided and not "default"
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice  

    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    json_data = {'text': text}

    response = requests.post(api_url, headers=headers, json=json_data)
    logging.info(f"Text-to-Speech response: {response}")
    return response.content  # Return the audio data

# Function to process user messages with OpenAI's GPT
def openai_process_message(user_message):
    """
    Processes a user message with OpenAI's GPT-3.5-turbo model.

    Args:
        user_message (str): The user's input message.

    Returns:
        str: The generated response from GPT-3.5-turbo.
    """

    prompt = """Act like a personal assistant. You can respond to questions, 
    translate sentences, summarize news, and give recommendations."""
    
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4000
    )

    logging.info(f"OpenAI response: {openai_response}")
    response_text = openai_response.choices[0].message.content
    return response_text