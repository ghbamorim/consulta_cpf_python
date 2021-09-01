from requests.models import Response
from app import port
import requests
import json
from flask import Flask, request, Response, jsonify
from base64 import b64encode

uri = "http://127.0.0.1:{}".format(port)

token = ""


def test_login():
    global token
    userAndPass = b64encode(b"user01:123456").decode("ascii")

    headers = {"authorization": 'Basic %s' % userAndPass}

    #response = requests.get(url=uri + "/login", headers=headers)
    app = Flask(__name__)

    client = app.test_client()
    response = client.get('/login', headers=headers)

    result = response.get_data()

    #token = result["token"]
    assert response.status_code == 200 and token is not None