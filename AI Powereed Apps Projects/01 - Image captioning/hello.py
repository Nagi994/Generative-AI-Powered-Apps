import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    gr.Markdown("## Simple Greeting App")  # Added a title for better presentation
    with gr.Row():  # Organizes the input and output nicely in a row
        name_input = gr.Textbox(label="Enter your name")
        output = gr.Textbox(label="Greeting")
    greet_button = gr.Button("Greet")  # A button to trigger the greeting
    greet_button.click(fn=greet, inputs=name_input, outputs=output)

demo.launch(server_name="0.0.0.0", server_port=8000) 