from requests.models import Response
from app import create_app
import json
from base64 import b64encode

token = ""


def test_login():
    global token
    userAndPass = b64encode(b"user01:123456").decode("ascii")

    headers = {"authorization": 'Basic %s' % userAndPass}

    app = create_app()

    client = app.test_client()
    response = client.get('/login', headers=headers)

    result = json.loads(response.get_data())

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

    app = create_app()

    client = app.test_client()
    response = client.get("/cpfstatus", headers=headers, json=body)
    result = json.loads(response.get_data())

    assert response.status_code == 200 and token is not None and "status" in result
