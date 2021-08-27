import json
from flask import Flask, request, Response
from interfaces.serpro import Serpro_intf
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route("/dadosCpf", methods=['GET'])
def getCpf():
    body = request.get_json()
    print(body)
    try:
      serpro_intf = Serpro_intf()
      return json.dumps(serpro_intf.consultaCpf(body["cpf"]))

    except Exception as e:
        print('Erro:', e)
        return Response(json.dumps( {'error': str(e)}), status=500, mimetype='application/json')

if __name__ == '__main__':
  app.run(debug=True)