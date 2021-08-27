import json
from flask import Flask, request
from interfaces.serpro import consultaCpf
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/dadosCpf", methods=['GET'])
def getCpf():
    body = request.get_json()
    print(body)
    return json.dumps(consultaCpf(body['cpf']))

if __name__ == '__main__':
  app.run(debug=True)