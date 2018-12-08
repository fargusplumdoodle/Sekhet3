#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

data = open('data.json', 'r')
data = json.loads(data.read())

class SekhnetAPI(Resource):
    def get(self, name):
        if name in data:
            return data[name], 200
        else:
            return "Resource not found", 404,  {'Access-Control-Allow-Origin': '*'}

    def post(self, name):
        return "Post not configured", 500
    def put(self, name):
        return "Put not configured", 500
    def delete(self, name):
        return "delete not configured", 500

api.add_resource(SekhnetAPI, "/<string:name>")
app.run(host='0.0.0.0', port=3004, debug=True)
