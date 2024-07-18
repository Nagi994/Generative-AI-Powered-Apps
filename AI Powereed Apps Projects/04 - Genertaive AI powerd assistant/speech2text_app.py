#!/usr/bin/env python3
# Shebang: Directs the operating system to use the Python3 interpreter.

# Import Statements
import torch       # PyTorch: A deep learning library used by the Transformers pipeline.
from transformers import pipeline  # Pipeline: Streamlines the process of loading and using pre-trained models.
import gradio as gr  # Gradio: A library for building easy-to-use web interfaces for ML models.

# Transcription Function
def transcript_audio(audio_file):
    """
    This function takes an audio file path as input, transcribes it using the OpenAI Whisper model, 
    and returns the transcribed text.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: The transcribed text from the audio file.
    """

    # Initialize the Speech Recognition Pipeline
    pipe = pipeline(
        "automatic-speech-recognition",  # Task: Automatic speech recognition.
        model="openai/whisper-tiny.en",   # Model: The Whisper model for English language.
        chunk_length_s=30                 # Chunk Length: Process audio in 30-second chunks.
    )

    # Transcribe the Audio
    result = pipe(audio_file, batch_size=8)["text"]  # Transcribe using batch processing.

    return result 

# Gradio Interface Setup
audio_input = gr.Audio(sources="upload", type="filepath") 
# Creates an audio input component that allows the user to upload an audio file.
# - sources="upload": Specifies that the audio will be uploaded from the user's machine.
# - type="filepath": The component will return the file path of the uploaded audio.

output_text = gr.Textbox()   
# Creates a textbox output component to display the transcribed text.

# Build the Gradio Interface
iface = gr.Interface(
    fn=transcript_audio,           # The function to be called when the "Submit" button is clicked.
    inputs=audio_input,           # The input component for the user to upload the audio file.
    outputs=output_text,          # The output component to display the transcribed text.
    title="Audio Transcription App",     # Title of the Gradio application.
    description="Upload the audio file" # Description/instructions for the user.
)

# Launch the Gradio App
if __name__ == "__main__":       
    # This line ensures that the following code is only executed if this script is run as the main program (not imported as a module).
    iface.launch(server_name="0.0.0.0", server_port=7860)  
    # Starts the Gradio app:
    # - server_name="0.0.0.0": Makes the app accessible from any device on the network.
    # - server_port=7860: Specifies the port on which the app will run.