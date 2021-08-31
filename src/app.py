import json
from flask import Flask, request, Response, jsonify
from interfaces.serpro import Serpro_intf
from models.params import Cpf_params
import jwt
import datetime
from db.fakedb import Db
from utils.auth import token_required
import datetime

app = Flask(__name__)

app.config["SECRET"] = "SECRET_KEY"
#tempo de duração do token
app.config["TOKEN_EXPIRES_IN"] = 30

db = Db()


@app.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    user_name = auth.username
    password = auth.password

    user = db.find_user(user_name, password)
    if user:
        token = jwt.encode(
            {
                "public_id":
                user.id,
                "exp":
                datetime.datetime.utcnow() +
                datetime.timedelta(minutes=app.config["TOKEN_EXPIRES_IN"])
            },
            app.config["SECRET"],
            algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"message": "invalid login or password"}), 401


@app.route("/cpfstatus", methods=["GET"])
@token_required
def getCpf(user):
    body = request.get_json()
    print(body)
    try:

        cpf_params = Cpf_params()
        cpf_params.client_id = body["client_id"]
        cpf_params.client_secret = body["client_secret"]
        cpf_params.user_cpf = body["user_cpf"]
        cpf_params.cpf_for_query = body["cpf"]

        serpro_intf = Serpro_intf()

        result, raw, status_code = serpro_intf.consultaCpf(cpf_params)

        print(
            "Time: {} - cpf: {} - Serpro return: {} - Status code: {}".format(
                datetime.datetime.now(), cpf_params.cpf_for_query, raw,
                status_code))

        return json.dumps(result)

    except Exception as e:
        print("Erro:", e)
        return Response(json.dumps({"error": {
            "reason": str(e)
        }}),
                        status=500,
                        mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
