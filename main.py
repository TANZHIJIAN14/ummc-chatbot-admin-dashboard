import gradio as gr
import pandas

from css import custom_css
from feedbackDb import get_feedback
from fileDb import get_files, get_file_by_gradio_file_path, delete_file, upload_files


def app_load(files_state, feedback_state):
    files_state = get_files()
    feedback_state = get_all_feedback()
    return files_state, feedback_state

# File Management ---------------
def upload_pdfs(file, state):
    try:
        upload_files(file)
        state.extend(file)
        return None, state, state
    except Exception as e:
        print(f"Error: {e}")
        gr.Error('Failed to upload file', duration=3)
        return file, state, state

def update_dashboard(state):
    print("Upload on change")
    uploaded_files = get_files()
    state = uploaded_files
    gr.Info('Successfully uploaded file', duration=3)
    return state

def delete(file, state):
    print(f"Delete:  {file}")
    uploaded_file = get_file_by_gradio_file_path(file)
    uploaded_file_id = str(uploaded_file["_id"])

    try:
        delete_file(uploaded_file_id)
        state = get_files()
        gr.Info('Successfully delete file', duration=3)
        return state
    except Exception as e:
        gr.Error('Failed to delete file', duration=3)
        return file

# Feedback Management ---------------
def get_all_feedback():
    try:
        dataset = get_feedback()
        return pandas.DataFrame(dataset)
    except Exception as e:
        gr.Error('Failed to get feedback', duration=3)

# Gradio Interface
with gr.Blocks(css=custom_css) as app:
    uploaded_files_state = gr.State(value=[])  # State to track uploaded files
    get_feedback_state = gr.State(value=[])

    with gr.Tab("File Management"):
        with gr.Row():
            # Upload column
            with gr.Column(scale=1):
                # gr.Markdown("## Upload a PDF File")
                pdf_upload = gr.File(label="Upload your PDF", file_types=[".pdf"], file_count="multiple")
                process_button = gr.Button("Upload")

            # Dashboard column
            with gr.Column(scale=2):
                # gr.Markdown("## Dashboard")
                pdf_preview = gr.Files(label="Uploaded PDF")

    with gr.Tab("Feedback"):
        gr.Markdown("## Dashboard")

        table_view = gr.DataFrame(
            value=get_feedback_state.value,
            headers=["_id", "user_id", "message", "created_at"],  # Column headers
            datatype=["str", "str", "str", "str"],
            elem_id="dataframe-container"
        )

    # App loading state
    app.load(app_load,
             inputs=[uploaded_files_state, get_feedback_state],
             outputs=[pdf_preview, table_view])

    # File Management Function-----------
    # Process uploaded file and update dashboard
    process_button.click(
        upload_pdfs,
        inputs=[pdf_upload, uploaded_files_state],
        outputs=[pdf_upload, pdf_preview, uploaded_files_state],
    )

    # Update the dashboard display whenever the state changes
    uploaded_files_state.change(
        update_dashboard,
        inputs=[uploaded_files_state],
        outputs=[pdf_preview],
    )

    # Delete file in file preview
    pdf_preview.delete(
        delete,
        inputs=[pdf_preview, uploaded_files_state],
        outputs=[pdf_preview]
    )

# Launch the app
app.launch(auth=("", ""))
# app.launch(share=True, auth=("", ""))
