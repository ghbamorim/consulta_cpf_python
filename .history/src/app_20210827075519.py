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
    try:
      return json.dumps(consultaCpf(body["cpf"]))

    except Exception as e:
        print('Erro ao recuperar token:', e)
        return str(e)

if __name__ == '__main__':
  app.run(debug=True)