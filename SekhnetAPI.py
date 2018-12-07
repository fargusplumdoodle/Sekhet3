#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

data = open('data.json', 'r')
data = json.loads(data.read())

class SekhnetAPI(Resource):
    def get(self, name):
        if name in data:
            return data[name], 200
        else:
            return "Resource not found", 404

    def post(self, name):
        return "Post not configured", 500
    def put(self, name):
        return "Put not configured", 500
    def delete(self, name):
        return "delete not configured", 500

api.add_resource(SekhnetAPI, "/<string:name>")
app.run(debug=True)
