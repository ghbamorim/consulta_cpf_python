from flask import Flask
from interfaces.serpro import consultaCpf
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/")
def getCpf():
    return consultaCpf('00993162428')

if __name__ == '__main__':
  app.run(debug=True)