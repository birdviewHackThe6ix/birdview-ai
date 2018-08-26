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
from PIL import Image, ImageDraw

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
        return result[0]['formatted_address']


# Cropping picture
    def get_crop_hint(self, path):
        """Detect crop hints on a single image and return the first result."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = Vtypes.Image(content=content)
# 2.3
        crop_hints_params = Vtypes.CropHintsParams(aspect_ratios=[0.3])
        image_context = Vtypes.ImageContext(crop_hints_params=crop_hints_params)

        response = client.crop_hints(image=image, image_context=image_context)
        hints = response.crop_hints_annotation.crop_hints

        # Get bounds for the first crop hint using an aspect ratio of 1.77.
        vertices = hints[0].bounding_poly.vertices

        return vertices

    def draw_hint(self, image_file):
        """Draw a border around the image using the hints in the vector list."""
        vects = self.get_crop_hint(image_file)

        im = Image.open(image_file)
        draw = ImageDraw.Draw(im)
        draw.polygon([
            vects[0].x, vects[0].y,
            vects[1].x, vects[1].y,
            vects[2].x, vects[2].y,
            vects[3].x, vects[3].y], None, 'red')
        im.save('/Users/alaashamandy/Desktop/output-hint.jpg', 'JPEG')

    def crop_to_hint(self, image_file):
        """Crop the image using the hints in the vector list."""
        vects = self.get_crop_hint(image_file)

        im = Image.open(image_file)
        im2 = im.crop([vects[0].x, vects[0].y,
                      vects[2].x - 1, vects[2].y - 1])
        im2.save('/Users/alaashamandy/Desktop/output-crop.jpg', 'JPEG')
