import json
from flask import Flask, request
from interfaces.serpro import consultaCpf
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/dadosCpf", methods=['GET'])
def getCpf():
    body = request.get_json()
    return json.dumps(consultaCpf('00993162428'))

if __name__ == '__main__':
  app.run(debug=True)