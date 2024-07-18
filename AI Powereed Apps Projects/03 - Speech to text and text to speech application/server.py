import base64
import json
import logging
import os
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import werkzeug 

# Initialize Flask App and Logging
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS
logging.basicConfig(level=logging.INFO)  # Configure logging

# Route for the main page
@app.route('/', methods=['GET'])
def index():
    """Renders the main HTML page."""
    return render_template('index.html')  

# Route for speech-to-text conversion
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    """Handles speech-to-text conversion requests."""
    logging.info("Processing speech-to-text request.") 

    # Get audio data from request, handle errors
    try:
        audio_binary = request.data 
    except werkzeug.exceptions.BadRequest as e:
        logging.error(f"Invalid request data: {e}")
        return "Bad Request", 400  # Return 400 status on bad request

    # Convert audio to text
    text = speech_to_text(audio_binary)  

    # Create JSON response with the transcribed text
    response = app.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )
    logging.info(response) 
    return response


# Route to process user messages with OpenAI and generate speech
@app.route('/process-message', methods=['POST'])
def process_message_route():
    """Handles user messages, sends them to OpenAI, and returns the response in text and speech format."""
    logging.info("Processing message request.")
    # Get user message and voice preference
    user_message = request.json['userMessage'] 
    voice = request.json['voice'] 

    logging.info(f"User message: {user_message}")
    logging.info(f"Selected voice: {voice}")

    # Process the message with OpenAI
    openai_response_text = openai_process_message(user_message)
    # Remove empty lines for cleaner output
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

    # Convert OpenAI's response to speech
    openai_response_speech = text_to_speech(openai_response_text, voice)
    # Encode speech audio as base64
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

    # Create JSON response with text and speech representations of the OpenAI response
    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    logging.info(response)
    return response



if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')  # Start the Flask app on port 8000
