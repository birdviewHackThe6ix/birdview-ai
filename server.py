from flask import Flask
from flask import request
from flask import Response
from flask import jsonify


from gcp_client import GCPClient

gcp_client = GCPClient()

app = Flask(__name__)

@app.route("/")
def status():
    return "Hello from BirdView-AI!"

@app.route("/nlu", methods=['POST', 'GET'])
def process():
    nlu_response = gcp_client.analyze_text(request.args.get('text', ''))
    js = jsonify(nlu_response)
    js.status_code = 200
    return js
