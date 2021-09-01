port = 5000


def create_app():
    import json
    from flask import Flask, request, Response, jsonify
    from interfaces.serpro import Serpro_intf
    from models.params import Cpf_params
    import datetime
    from db.fakedb import Db
    import datetime
    import jwt
    from functools import wraps

    app = Flask(__name__)

    app.config["SECRET"] = "SECRET_KEY"
    #tempo de duração do token
    app.config["TOKEN_EXPIRES_IN"] = 30

    db = Db()

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "x-access-token" in request.headers:
                token = request.headers["x-access-token"]

            if not token:
                return jsonify({"message": "Missing token"}), 401

            try:
                jwt_data = jwt.decode(token,
                                      app.config["SECRET"],
                                      algorithms="HS256")
                user = db.find_by_id(jwt_data["public_id"])
                if not user:
                    return jsonify({"message": "Invalid token"}), 401
            except:
                return jsonify({"message": "Invalid token"}), 401
            return f(user, *args, **kwargs)

        return decorated

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
            return jsonify({"token": token}), 200
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

            print("Time: {} - cpf: {} - Serpro return: {} - Status code: {}".
                  format(datetime.datetime.now(), cpf_params.cpf_for_query,
                         raw, status_code))

            return json.dumps(result), 200

        except Exception as e:
            print("Erro:", e)
            return Response(json.dumps({"error": {
                "reason": str(e)
            }}),
                            status=500,
                            mimetype="application/json")

    return app


if __name__ == "__main__":
    create_app().run(host='localhost', port=port, debug=True)
