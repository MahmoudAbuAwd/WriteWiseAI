import gradio as gr
from models.grammar import correct_grammar
from models.style import paraphrase
from models.generate import generate_text

def handle_all(text, task):
    if not text.strip():
        return "⚠️ Please enter some text to process!"
    
    try:
        if task == "Grammar Correction":
            result = correct_grammar(text)
            return f"✅ **Grammar Corrected:**\n\n{result}"
        elif task == "Style Improvement":
            result = paraphrase(text)
            return f"✨ **Style Enhanced:**\n\n{result}"
        elif task == "Content Generation":
            result = generate_text(text)
            return f"🚀 **Generated Content:**\n\n{result}"
        else:
            return "❌ Invalid option selected."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}\nPlease try again with different text."

def get_example_text(task):
    examples = {
        "Grammar Correction": "this is a sample text with some grammar mistake that need to be fix.",
        "Style Improvement": "The meeting was good. We talked about many things. It was productive.",
        "Content Generation": "Write a creative story about a robot learning to paint"
    }
    return examples.get(task, "")

# Custom CSS for better styling
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-text {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 0.5em;
}

.description-text {
    text-align: center;
    font-size: 1.2em;
    color: #666;
    margin-bottom: 2em;
    line-height: 1.6;
}

.task-info {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}

.footer-text {
    text-align: center;
    color: #888;
    font-size: 0.9em;
    margin-top: 2em;
}
"""

# Create the interface with enhanced features
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as interface:
    
    # Header
    gr.HTML("""
        <div class="header-text">
            🧠 WriteWiseAI
        </div>
        <div class="description-text">
            Your intelligent writing companion powered by advanced AI models<br>
            ✨ Perfect grammar • 🎨 Beautiful style • 🚀 Creative content
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input section
            gr.HTML("<h3>📝 Input</h3>")
            
            task_selector = gr.Radio(
                choices=["Grammar Correction", "Style Improvement", "Content Generation"],
                label="🎯 Choose Your Task",
                value="Grammar Correction",
                info="Select what you'd like WriteWiseAI to help you with"
            )
            
            input_text = gr.Textbox(
                lines=8,
                placeholder="Enter your text or prompt here...",
                label="Your Text",
                info="Paste your content here or use the example button below"
            )
            
            with gr.Row():
                process_btn = gr.Button("🚀 Process Text", variant="primary", size="lg")
                example_btn = gr.Button("💡 Load Example", variant="secondary")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")
        
        with gr.Column(scale=2):
            # Output section
            gr.HTML("<h3>✨ Result</h3>")
            
            output_text = gr.Textbox(
                lines=8,
                label="Processed Text",
                info="Your enhanced text will appear here",
                interactive=False
            )
            
            with gr.Row():
                copy_btn = gr.Button("📋 Copy Result", variant="secondary")
                new_task_btn = gr.Button("🔄 Process Again", variant="secondary")
    
    # Task descriptions
    gr.HTML("""
        <div class="task-info">
            <h4>🎯 Task Descriptions:</h4>
            <p><strong>📝 Grammar Correction:</strong> Fix spelling, grammar, and punctuation errors while preserving your original meaning.</p>
            <p><strong>✨ Style Improvement:</strong> Enhance readability, flow, and overall writing quality with better word choices.</p>
            <p><strong>🚀 Content Generation:</strong> Create new content based on your prompts and ideas.</p>
        </div>
    """)
    
    # Event handlers
    def load_example(task):
        return get_example_text(task)
    
    def clear_inputs():
        return "", ""
    
    def copy_to_clipboard(text):
        return gr.Info("Text copied to clipboard! 📋")
    
    # Connect the events
    process_btn.click(
        fn=handle_all,
        inputs=[input_text, task_selector],
        outputs=output_text
    )
    
    example_btn.click(
        fn=load_example,
        inputs=task_selector,
        outputs=input_text
    )
    
    clear_btn.click(
        fn=clear_inputs,
        outputs=[input_text, output_text]
    )
    
    new_task_btn.click(
        fn=lambda: "",
        outputs=input_text
    )
    
    # Auto-update example when task changes
    task_selector.change(
        fn=lambda task: f"Current task: {task}. Click 'Load Example' to see a sample input.",
        inputs=task_selector,
        outputs=None
    )
    
    # Footer
    gr.HTML("""
        <div class="footer-text">
            Made with ❤️ using Gradio and Hugging Face Models<br>
            <em>Empowering writers with AI technology</em>
        </div>
    """)

if __name__ == "__main__":
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        favicon_path=None,
        inbrowser=True
    )