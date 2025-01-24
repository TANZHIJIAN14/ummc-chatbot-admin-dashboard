import gradio as gr
import pandas
from css import custom_css
from feedbackDb import get_feedback
from fileDb import get_files, get_file_by_gradio_file_path, delete_file, upload_files
from uploadUrlDb import upload_url_as_pdf, get_url_as_pdf


def app_load():
    uploaded_files_state.value = get_files()
    get_feedback_state.value = get_all_feedback()
    return uploaded_files_state.value, get_feedback_state.value

# File Management ---------------
def upload_url(name, url):
    try:
        if not name.strip():
            gr.Warning("Name cannot be empty.", duration=3)
            return name, url, None
        if not url.strip():
            gr.Warning("URL cannot be empty.", duration=3)
            return name, url, None

        resp = upload_url_as_pdf(url, name)
        if not resp:
            raise Exception

        pdf_temp_file_path = get_url_as_pdf(resp['url'])
        if not pdf_temp_file_path:
            raise Exception

        return None, None, [pdf_temp_file_path]
    except Exception as e:
        gr.Error('Failed to upload url as pdf', duration=3)
        return name, url, None

def upload_pdfs(file):
    try:
        if not file:
            gr.Warning("No selected file to be uploaded.", duration=3)
            return file, uploaded_files_state.value, uploaded_files_state

        upload_files(file)
        uploaded_files_state.value.extend(file)
        gr.Info('Successfully uploaded file', duration=3)
        return None, uploaded_files_state.value
    except Exception as e:
        print(f"Error: {e}")
        gr.Error('Failed to upload file', duration=3)
        return file, uploaded_files_state.value

# def update_dashboard(state):
#     print("Upload on change")
#     uploaded_files = get_files()
#     state = uploaded_files
#     gr.Info('Successfully uploaded file', duration=3)
#     return state

def delete(deleted_file: gr.DeletedFileData):
    try:
        uploaded_file = get_file_by_gradio_file_path(deleted_file.file.path)
        uploaded_file_id = str(uploaded_file["_id"])

        delete_file(uploaded_file_id)
        uploaded_files_state.value = get_files()
        gr.Info('Successfully delete file', duration=3)
        return uploaded_files_state.value
    except Exception as e:
        gr.Error('Failed to delete file', duration=3)
        return uploaded_files_state.value

# Feedback Management ---------------
def get_all_feedback():
    try:
        dataset = get_feedback()
        return pandas.DataFrame(dataset)
    except Exception as e:
        gr.Error('Failed to get feedback', duration=3)

# Gradio Interface
with gr.Blocks(css=custom_css) as app:
    app.title = "Admin dashboard"

    uploaded_files_state = gr.State(value=[])  # State to track uploaded files
    get_feedback_state = gr.State(value=[])

    with gr.Tab("File Management"):
        gr.Markdown("# Upload URL as PDF")
        with gr.Column():
            with gr.Row():
                name_input = gr.Textbox(label="Name", placeholder="Enter your name")
                url_input = gr.Textbox(label="URL", placeholder="Enter the URL")
            with gr.Column():
                submit_button = gr.Button("Upload")
        with gr.Row():
            # Upload column
            with gr.Column(scale=1):
                pdf_upload = gr.File(label="Upload your PDF", file_types=[".pdf"], file_count="multiple")
                process_button = gr.Button("Upload")

            # Dashboard column
            with gr.Column(scale=2):
                pdf_preview = gr.Files(label="Uploaded PDF", interactive=True)

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
             inputs=None,
             outputs=[pdf_preview, table_view])

    # File Management Function-----------
    # Link the button to the function
    submit_button.click(
        upload_url,
        inputs=[name_input, url_input],
        outputs=[name_input, url_input, pdf_upload])

    # Process uploaded file and update dashboard
    process_button.click(
        upload_pdfs,
        inputs=[pdf_upload],
        outputs=[pdf_upload, pdf_preview],
    )

    # Delete file in file preview
    pdf_preview.delete(
        delete,
        None,
        outputs=[pdf_preview]
    )

# Launch the app
# app.launch()
app.launch(share=True, auth=("test", "test"))
