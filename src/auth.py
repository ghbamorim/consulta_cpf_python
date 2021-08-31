from flask import request, jsonify
import jwt
from fakedb import Db
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Missing token"}), 401
        from app import app, db

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