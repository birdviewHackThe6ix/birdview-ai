from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

# Imports clients
from gcp_client import GCPClient
from aws_client import AWSClient


from pymongo import MongoClient



from NaturalLanguageProcessing.processor import Processor

# Cloud clients
gcp_client = GCPClient()
aws_client = AWSClient()

import ssl

client = MongoClient("mongodb://birdview_client:birdy123@cluster0-shard-00-00-eupui.gcp.mongodb.net:27017,cluster0-shard-00-01-eupui.gcp.mongodb.net:27017,cluster0-shard-00-02-eupui.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client['test']
profiles_collection = db['profiles']

# Utils
nlp = Processor()

app = Flask(__name__)

@app.route("/")
def status():
    return "Hello from BirdView-AI!"

@app.route("/new-profile", methods=['POST', 'GET'])
def index_new_profile():
    mongo_id = request.args.get('id', '')
    filename = request.args.get('filename', '')
    hashes = aws_client.index_faces(filename)
    collection.update({'_id': mongo_id},
                {
                    '$set': {'hash': hashes[0]}
                })
    js = jsonify('Indexed')
    js.headers['Access-Control-Allow-Origin'] = '*'
    js.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return js



@app.route("/nlu", methods=['POST', 'GET'])
def process():
	# Get params
    text = request.args.get('text', '')
    mongo_id = request.args.get('id', '')
    name_from_hashtag = request.args.get('hashtag', '')
    filename = request.args.get('filename', '')


    # Analyze text
    if text:
        nlu_response = gcp_client.analyze_text(request.args.get('text', ''))
        approx_address = nlp.form_address_from_components(nlu_response['entities'])
        formatted_address = gcp_client.geocode(approx_address)
        text = '{} was at {}'.format(name_from_hashtag, formatted_address)
        tag =name_from_hashtag + 'BirdView'
        profiles_collection.update({'hashtag': tag},
                        {
                            '$push': {
                                'matches': {
                                    'text': text
                                }
                            }
                        })

    if filename:
        matches = aws_client.detect_faces(filename)
        for match in matches:
            profiles_collection.update({'hash': match},
                {
                    '$push': {
                        'matches': {
                            'imgurl': filename
                        }
                    }
                })

    js = jsonify({'response': "Thank you for submitting your request. The police will be in contact with you once your child has been found."})
    js.status_code = 200
    js.headers['Access-Control-Allow-Origin'] = '*'
    js.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return js
