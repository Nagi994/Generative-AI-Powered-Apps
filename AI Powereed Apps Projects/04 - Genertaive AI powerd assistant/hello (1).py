import gradio as gr  # Import the Gradio library for creating web interfaces.

# Function to generate greeting
def greet(name):
    """
    This function takes a name as input and returns a personalized greeting message.

    Args:
        name (str): The name to be greeted.

    Returns:
        str: A greeting message in the format "Hello <name>!".
    """
    return f"Hello {name}!"  # Use f-string for clean string formatting.

# Create the Gradio Interface
demo = gr.Interface(
    fn=greet,             # The function to be called when the interface is used.
    inputs="text",        # Specifies a text input component for the user to enter their name.
    outputs="text",       # Specifies a text output component to display the greeting message.
    title="Simple Greeting App",  # The title of the Gradio app in the web interface.
    description="Type your name and get a greeting!",  # A description/instructions for the user.
)

# Launch the Gradio App
if __name__ == "__main__":    
    # Ensure this code runs only when executed directly as a script, not when imported.
    demo.launch(
        server_name="0.0.0.0",  # Listen on all network interfaces (0.0.0.0)
        server_port=7860        # Run the app on port 7860
    )