from flask import Flask
from flask import request
from flask import Response
from flask import jsonify


from gcp_client import GCPClient
from PIL import Image

from pymongo import MongoClient

gcp_client = GCPClient()

client = MongoClient()
db = client['TEST_DB']

app = Flask(__name__)

@app.route("/")
def status():
    return "Hello from BirdView-AI!"

@app.route("/nlu", methods=['POST', 'GET'])
def process():
	# Get text
    nlu_response = gcp_client.analyze_text(request.args.get('text', ''))

    # Get Image
    img = Image.open(request.files['file'])
    path = '/Users/alaashamandy/Desktop/ourfile.jpg'
    img.save(path)
    image_response = gcp_client.predictPerson(path)

    if (image_response['score'] > 0.8 and image_response['name'] != 'None_of_the_above'):
    	collection = db['matches']
    	match = {'Name': image_response['name'], 'Path': path, 'Confidence': image_response['score'], 'Text': request.args.get('text', ''), 'Entities': nlu_response['entities'], 'Sentiment': nlu_response['sentiment']}
    	collection.insert_one(match)

    	# CONTACT POLICE HERE


    # formulate response
    # final_response = {"nlu_result": nlu_response, "image_result": image_response}

    # js = jsonify(final_response)
    js = jsonify({'response': "Thank you for submitting your request. The police will be in contact with you once your child has been found."})
    js.status_code = 200
    return js
