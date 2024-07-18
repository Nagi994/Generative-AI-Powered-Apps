from flask import Flask, request, render_template
from flask_cors import CORS
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for requests from other origins (e.g., your frontend)

# Load Pre-Trained Model and Tokenizer 
model_name = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Conversation History (Moved outside the route for persistence across requests)
conversation_history = [] 


# Route for Rendering the Main Page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')  # Assumes you have an index.html file for the UI


# Route for Handling Chatbot Interactions
@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    global conversation_history  # Make sure we're modifying the global history

    data = request.get_data(as_text=True)
    data = json.loads(data)
    
    input_text = data['prompt']

    # Construct Conversation History (Optimized)
    history_string = "\n".join(conversation_history)

    # Tokenization and Model Inference
    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
    outputs = model.generate(**inputs)

    # Decode the Response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Update Conversation History
    conversation_history.append(input_text)
    conversation_history.append(response)

    return response  # Send the response back as text


if __name__ == '__main__':
    app.run(debug=True) 