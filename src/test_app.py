from requests.models import Response
from app import login
import requests
import json
from base64 import b64encode

uri = "http://127.0.0.1:5000"

token = ""


def test_login():
    global token
    userAndPass = b64encode(b"user01:123456").decode("ascii")

    headers = {"authorization": 'Basic %s' % userAndPass}

    response = requests.get(url=uri + "/login", headers=headers)
    result = json.loads(response.content)

    token = result["token"]
    assert response.status_code == 200 and token is not None


def test_cpfstatus():
    global token
    headers = {"x-access-token": token}

    body = {
        "client_id": "8ddc46f2-f6a3-4077-9e04-74b55de934a5",
        "client_secret": "06d4aaac-1412-45f6-bd7c-38b2bef0d706",
        "user_cpf": "77689062768",
        "cpf": "77689062768"
    }

    response = requests.get(url=uri + "/cpfstatus", headers=headers, json=body)
    result = json.loads(response.content)

    print(result)
    assert response.status_code == 200 and token is not None and "status" in result
