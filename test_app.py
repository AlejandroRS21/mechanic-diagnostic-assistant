"""
Minimal test version of app.py
"""
import gradio as gr

print("✅ Gradio imported")

# Simple interface
with gr.Blocks(title="Test") as demo:
    gr.Markdown("# 🔧 Test Interface")
    
    chatbot = gr.Chatbot(label="Chat")
    msg = gr.Textbox(label="Message")
    btn = gr.Button("Send")
    
    def respond(message, history):
        history = history or []
        # Gradio 6.0 format: list of dicts with 'role' and 'content'
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"Echo: {message}"})
        return history, ""
    
    btn.click(respond, [msg, chatbot], [chatbot, msg])

print("✅ Interface created")

if __name__ == "__main__":
    print("🚀 Launching...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
