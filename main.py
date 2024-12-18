import gradio as gr
from db import upload_file, get_files

def app_load(state):
    state = get_files()
    return state

def upload_pdf(file, state):
    try:
        upload_file(file)
        state.append(file)
        return state, state
    except Exception as e:
        print(f"Error: {e}")
        return file, state


def update_dashboard(state):
    print("Upload on change")
    uploaded_files = get_files()
    state = uploaded_files
    return state

# Gradio Interface
with gr.Blocks() as app:
    uploaded_files_state = gr.State(value=[])  # State to track uploaded files

    with gr.Row():
        # Upload column
        with gr.Column(scale=1):
            gr.Markdown("## Upload a PDF File")
            pdf_upload = gr.File(label="Upload your PDF", file_types=[".pdf"])
            process_button = gr.Button("Upload")

        # Dashboard column
        with gr.Column(scale=2):
            gr.Markdown("## Dashboard")
            pdf_preview = gr.Files(label="Uploaded PDF")

    # Process uploaded file and update dashboard
    process_button.click(
        upload_pdf,
        inputs=[pdf_upload, uploaded_files_state],
        outputs=[pdf_preview, uploaded_files_state],
    )

    # Update the dashboard display whenever the state changes
    uploaded_files_state.change(
        update_dashboard,
        inputs=[uploaded_files_state],
        outputs=[pdf_preview],
    )

    app.load(app_load, inputs=uploaded_files_state, outputs=pdf_preview)

# Launch the app
app.launch()
