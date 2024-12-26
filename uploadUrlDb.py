import io
import os
import tempfile
from http import HTTPStatus
from urllib.parse import urlparse

import requests
from constant import BACKEND_URL

def upload_url_as_pdf(raw_url, name):
    try:
        url = f"{BACKEND_URL}/convert/pdf-from-url"
        param = {
            "url": raw_url,
            "file_name": name
        }
        response = requests.post(url, params=param)

        if response.status_code == HTTPStatus.OK.value:
            return response.json()
        else:
            raise Exception(f"Failed to upload the url: {raw_url} with file name: {name}")
    except Exception as e:
        raise Exception(f"Upload url as pdf: Internal server error")

def get_url_as_pdf(pdf_url):
    try:
        file_name = extract_pdf_name_from_url(pdf_url)
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code != 200:
            return None, "Failed to download PDF from the provided URL"

        temp_pdf = save_pdf_with_custom_name(pdf_response, file_name)

        # print(f"Pdf from url: {temp_pdf}")
        return temp_pdf
    except Exception as e:
        raise Exception("Failed to get pdf from url")


def extract_pdf_name_from_url(pdf_url):
    # Parse the URL
    parsed_url = urlparse(pdf_url)
    # Extract the filename from the path
    file_name = os.path.basename(parsed_url.path)
    return file_name


def save_pdf_with_custom_name(pdf_response, custom_name):
    # Step 1: Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Step 2: Define the custom path for the temp PDF file
    custom_pdf_path = os.path.join(temp_dir, custom_name)

    # Step 3: Write the PDF content to the custom-named file
    with open(custom_pdf_path, 'wb') as f:
        f.write(pdf_response.content)

    return custom_pdf_path