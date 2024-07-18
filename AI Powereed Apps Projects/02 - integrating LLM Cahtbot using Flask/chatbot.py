from transformers import AutoTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM

# Model Configuration
model_name = "facebook/blenderbot-400M-distill"  # Specify the Blenderbot model to use

# Model Loading
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)  
# Load the pre-trained model (downloads it from the Hugging Face Hub if not already on your machine)

tokenizer = AutoTokenizer.from_pretrained(model_name)
# Load the tokenizer associated with the model (used for converting text to/from numbers)

conversation_history = []  # Initialize an empty list to store the conversation history

history_string = "\n".join(conversation_history)  # (No history yet, so this is an empty string)

# First Interaction (Outside the Loop)
input_text = "hello, how are you doing?"  # The user's initial message

# Tokenization and Model Inference
inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
# Combines history and input, tokenizes them, and prepares them in a format suitable for the model
# `return_tensors="pt"` returns PyTorch tensors

print(inputs)

tokenizer.pretrained_vocab_files_map
#print file locations

outputs = model.generate(**inputs)  
# Pass the tokenized inputs to the model for generating a response

# Response Decoding
response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()  
# Convert the model's output (numbers) back into text
# `skip_special_tokens=True` removes any special tokens the model might have added

print(response)

# Update Conversation History
conversation_history.append(input_text)
conversation_history.append(response)
print(conversation_history)


# Main Conversation Loop
while True: 
    history_string = "\n".join(conversation_history)  
    # Join the conversation history into a single string with newlines as separators

    input_text = input("> ")  
    # Prompt the user to enter their message

    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt") 
    # Tokenize the current input along with the entire conversation history

    outputs = model.generate(**inputs)  
    # Generate the model's response 

    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    # Decode the response

    print(response) 

    conversation_history.append(input_text)
    conversation_history.append(response)  
    # Add the user's input and the model's response to the conversation history 
