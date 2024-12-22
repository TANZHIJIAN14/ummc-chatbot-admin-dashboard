from http import HTTPStatus
import requests
from constant import BACKEND_URL

def get_feedback():
    url = f"{BACKEND_URL}/feedback/"
    response = requests.get(url)

    # Check the response status
    if response.status_code == HTTPStatus.OK.value:
        return response.json()
    else:
        raise Exception("Failed to get feedbacks")