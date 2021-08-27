from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/", ['GET'])
def getCpf(cpf):
    return "<p>Hello, World!</p>"
  
if __name__ == '__main__':
  app.run(debug=True)