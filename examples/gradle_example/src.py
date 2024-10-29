import gradio as gr
from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the classification function
def classify_text(text, labels):
    labels = labels.split(",")
    result = classifier(text, candidate_labels=labels)
    return {label: score for label, score in zip(result["labels"], result["scores"])}

# Create the Gradio interface
interface = gr.Interface(
    fn=classify_text,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter text here..."),
        gr.Textbox(lines=1, placeholder="Enter comma-separated labels here...")
    ],
    outputs=gr.Label(num_top_classes=3),
    title="Zero-Shot Text Classification",
    description="Classify text into labels without training data.",
)

# Launch the interface
interface.launch()
