import json
from flask import Flask, request, Response, jsonify, make_response
from interfaces.serpro import Serpro_intf, Cpf_params
from flask_restful import Api
import jwt
import datetime
from fake_db import Db

app = Flask(__name__)

app.config['SECRET'] = 'SECRET'

@app.route("/login", methods=['GET'])
def login():
  auth = request.authorization
  db = Db()
  db.init_fake_db()
  user = db.find_user(1, '123456')
  if user:
    token = jwt.encode({'public_id' : 'public_id', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET']), 200
    return jsonify({'token' : token})
  return jsonify({'message': 'invalid login or password'}), 401

@app.route("/dadosCpf", methods=['GET'])
def getCpf():
    body = request.get_json()
    print(body)
    try:

      cpf_params = Cpf_params()
      cpf_params.client_id = '8ddc46f2-f6a3-4077-9e04-74b55de934a5'
      cpf_params.client_secret = '06d4aaac-1412-45f6-bd7c-38b2bef0d706'
      cpf_params.user_cpf = '00993162428'
      cpf_params.cpfs_for_query = body["cpf"]

      serpro_intf = Serpro_intf()
      return json.dumps(serpro_intf.consultaCpf(cpf_params))

    except Exception as e:
        print('Erro:', e)
        return Response(json.dumps( {'error': str(e)}), status=500, mimetype='application/json')

#if __name__ == '__main__':
app.run(debug=True)