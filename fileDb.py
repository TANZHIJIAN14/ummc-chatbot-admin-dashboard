import os
from http import HTTPStatus
import requests
from constant import BACKEND_URL

def get_files():
    url = f"{BACKEND_URL}/upload/file"
    response = requests.get(url)

    # Check the response status
    if response.status_code == HTTPStatus.OK.value:
        files = response.json()

        # Extract file names assuming each file entry has a 'name' key
        file_paths = [file.get("gradio_file_path") for file in files]

        return file_paths
    else:
        raise Exception("Failed to get files")

def get_file_by_gradio_file_path(gradio_file_path):
    url = f"{BACKEND_URL}/upload/file/gradio_file_path"
    param = {"gradio_file_path": gradio_file_path}
    response = requests.get(url, params=param)

    # Check the response status
    if response.status_code == HTTPStatus.OK.value:
        return response.json()
    else:
        raise Exception(f"Failed to get file with given gradio file path: {gradio_file_path}")

def upload_files(file_paths):
    url = f"{BACKEND_URL}/upload/file/pdf"

    file_list = [
        ('files', (file_path, open(file_path, 'rb'), 'application/pdf'))
        for file_path in file_paths
    ]

    # Send the POST request
    response = requests.post(url, files=file_list)

    # Close all opened files
    for _, (filename, file_obj, _) in file_list:
        file_obj.close()

    # Check the response status
    if response.status_code == HTTPStatus.OK.value:
        return response.json()
    else:
        raise Exception(f"Failed to upload files: {response.json()}")

def delete_file(file_id):
    if not file_id:
        raise Exception("File id is required")

    url = f"{BACKEND_URL}/upload/file/pdf"
    param = {"file_id": file_id}
    response = requests.delete(url, params=param)

    if response.status_code != HTTPStatus.OK.value:
        raise Exception("Failed to delete file")