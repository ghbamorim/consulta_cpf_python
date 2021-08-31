import json
from flask import Flask, request, Response, jsonify, make_response
from interfaces.serpro import Serpro_intf, Cpf_params
from flask_restful import Api
import jwt
import datetime
from fake_db import Db
from functools import wraps

app = Flask(__name__)

app.config['SECRET'] = 'SECRET_KEY'
app.config['TOKEN_EXPIRES_IN'] = 30  #minutes

db = Db()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Missing token'}), 401

        jwt_data = jwt.decode(token, app.config['SECRET'], algorithms="HS256")

        try:
            user = db.find_by_id(jwt_data['public_id'])
            if not user:
                return jsonify({'message': 'Inválid token'}), 401
        except:
            return jsonify({'message': 'Inválid token'}), 401
        return f(user, *args, **kwargs)

    return decorated


@app.route("/login", methods=['GET'])
def login():
    auth = request.authorization
    user_name = auth.username
    password = auth.password

    user = db.find_user(user_name, password)
    if user:
        token = jwt.encode(
            {
                'public_id':
                user.id,
                'exp':
                datetime.datetime.utcnow() +
                datetime.timedelta(minutes=app.config['TOKEN_EXPIRES_IN'])
            },
            app.config['SECRET'],
            algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'invalid login or password'}), 401


@app.route("/dadosCpf", methods=['GET'])
@token_required
def getCpf(user):
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
        return Response(json.dumps({'error': str(e)}),
                        status=500,
                        mimetype='application/json')


#if __name__ == '__main__':
app.run(debug=True)