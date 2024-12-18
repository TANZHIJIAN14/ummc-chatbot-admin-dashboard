# MongoDB setup
import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

from constant import BACKEND_URL

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB_NAME")]  # Database name
users_collection = db["users"]  # Collection name

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

def upload_file(file_path):
    url = f"{BACKEND_URL}/upload/file/pdf"
    params = {
        "gradio_file_path": file_path
    }

    # Open the file in binary mode and prepare the payload
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file, 'application/pdf')}

        # Send the POST request
        response = requests.post(url, files=files, params=params)

    # Check the response status
    if response.status_code == HTTPStatus.OK.value:
        return response.json()
    else:
        raise Exception(f"Failed to upload file: {response.json()}")