import json
import logging
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
@app.route('/')
def hello():
  app.logger.info("A User entered")
  q = request.args.get('q')
  print(q)
  return "Hello"

@app.route('/users', methods=['GET'])
def display_data():
    app.logger.info("A User request for all users")
    jsonbody = {
        "users" : [],
    }
    with open('data.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        for item in data:
            jsonbody["users"].append(item)
        return jsonify(jsonbody)

@app.route("/add/<name>")
def add(name):
    app.logger.info("A User add a data")
    with open('data.txt', 'a') as f:
        f.write('\n'+name)
        f.close()
    jsonbody = {
        "users" : name,
    }
    return jsonify(jsonbody)

if __name__ == '__main__':
    app.run(port=8080,debug=False)