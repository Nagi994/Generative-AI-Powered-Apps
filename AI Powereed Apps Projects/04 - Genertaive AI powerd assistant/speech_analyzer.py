#!/usr/bin/env python3  

# Shebang: Directs the operating system to use the Python3 interpreter for executing this script.

# Import Statements
import torch  # PyTorch for deep learning and tensor operations.
import gradio as gr  # Gradio for creating user interfaces for machine learning models.

from transformers import pipeline  # Transformers library for easy access to pre-trained models.
from langchain.prompts import PromptTemplate  # Langchain to create structured prompts for language models.
from langchain.chains import LLMChain  # Langchain for chaining prompts and LLM responses together.

from ibm_watson_machine_learning.foundation_models import Model  # IBM SDK for interacting with foundation models.
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM  # LangChain wrapper for IBM Watsonx LLM.
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams  # Parameter names for text generation with IBM models.

# IBM Watson Model Setup
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",  # URL for the IBM Watson Machine Learning service.
    "apikey": "YOUR_API_KEY"  # Replace with your actual IBM Watson API key.
}
# Generation parameters for the language model
params = {
    GenParams.MAX_NEW_TOKENS: 800,    # Maximum number of tokens to generate in a single response.
    GenParams.TEMPERATURE: 0.1        # Controls randomness in text generation (lower = more focused).
}

# Load Llama 2 Chat Model
llama2_model = Model(
    model_id='meta-llama/llama-2-70b-chat',    # ID of the Llama 2 70B chat model on IBM Watson.
    credentials=my_credentials,             # Authentication credentials.
    params=params,                           # Text generation parameters.
    project_id="skills-network"              # Your project ID on IBM Watson Machine Learning.
)

# Create LangChain-compatible LLM object
llm = WatsonxLLM(llama2_model)                 # Creates an interface for using the model with LangChain.


# Prompt Template
prompt_template = """
<s><<SYS>>
List the key points with details from the context:
[INST] The context : {context} [/INST]
<</SYS>>
"""
# Explanation:
#  - <s><<SYS>>: Marks the beginning of the system message.
#  - [INST]: Marks the beginning of the instruction for the model.
#  - {context}: Placeholder for the input text.
#  - [/INST]: Marks the end of the instruction.
#  - <</SYS>>: Marks the end of the system message.

# Create a prompt object
prompt = PromptTemplate(
    input_variables=["context"],   # Defines the variable the prompt will take as input.
    template=prompt_template        # The template string for the prompt.
)

# Chain the LLM and the prompt together
chain = LLMChain(llm=llm, prompt=prompt)        # This creates a chain to manage the LLM and prompt.


# Audio Transcription and Summarization Function
def transcript_audio(audio_file):
    # Load Whisper model for speech-to-text
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny.en",  # English whisper model from OpenAI.
        chunk_length_s=30,               # Process audio in 30-second chunks.
    )

    # Transcribe the audio
    transcript_text = pipe(audio_file, batch_size=8)["text"]  # Transcribe and get the text.

    # Summarize with Llama 2 Model
    result = chain.run(transcript_text)      # Run the text through the LLM chain for summarization.
    return result


# Gradio Interface Setup
audio_input = gr.Audio(sources="upload", type="filepath")  # File upload component for audio.
output_text = gr.Textbox()                               # Textbox component to display results.

iface = gr.Interface(
    fn=transcript_audio,                         # Function to be called when the interface is run.
    inputs=audio_input,                         # Input component (audio file).
    outputs=output_text,                        # Output component (summarized text).
    title="Audio Transcription & Key Points App",  # Title of the web app.
    description="Upload an audio file to transcribe and extract key points."  # Description of the web app.
)

# Main Execution Block - Conditional starting point of the script
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)  # Start Gradio interface on all network interfaces, port 7860.
