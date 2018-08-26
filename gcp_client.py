#!/usr/bin/env python

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import argparse
import io
import os
# Image related imports

# Imports the Google Maps SDK
import googlemaps

# Credentials
MAPSAPIKEY = open(os.path.join('APIKEYS.txt'), 'r').readline().strip()

class GCPClient:
    def __init__(self):
        # Instantiates a client
        self.client = language.LanguageServiceClient()
        self.gmaps = googlemaps.Client(key=MAPSAPIKEY)

    def analyze_text(self, text):
        # Initialize a document object
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        # Define features to return
        features = {'extract_syntax': False, 'extract_entities': True,
            'extract_document_sentiment': True, 'classify_text': False}
        # Get entities and sentiment
        entities_response = self.client.analyze_entities(document=document, encoding_type='UTF32')
        sentiment_response = self.client.analyze_sentiment(document=document)
        # Define a result dict
        res = {'entities': [],
         'sentiment': sentiment_response.document_sentiment.score}
        # Refernence for entity types
        entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
        for entity in entities_response.entities:
            res['entities'].append({
                'name': entity.name,
                'type': entity_type[entity.type],
                'salience': entity.salience
            })
        return res

    # Geocoding an address
    def geocode(self, address_components):
        geocode_result = self.gmaps.geocode(address_components)
        return geocode_result[0]['formatted_address']
