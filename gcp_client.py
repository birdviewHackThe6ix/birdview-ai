#!/usr/bin/env python

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import argparse
import io
import os
from google.cloud import automl_v1beta1 as automl



class GCPClient:
    def __init__(self):
        # Instantiates a client
        self.client = language.LanguageServiceClient()

    def analyze_text(self, text):
        # Initialize a document object
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        # Get sentiment analysis
        features = {'extract_syntax': False, 'extract_entities': True,
            'extract_document_sentiment': True, 'classify_text': False}
        # Get entities and sentiment
        annotations = self.client.annotate_text(document=document, features=features)
        return {'sentiment': sentiment, 'annotations': annotations}
    
    def predict(self):
        """Make a prediction for an image."""
        # [START automl_vision_predict]
        # TODO(developer): Uncomment and set the following variables
        project_id = 'birdview-214413'
        compute_region = 'us-central1'
        model_id = 'ICN3754998888766534373'
        file_path = '/Users/alaashamandy/Desktop/testImage.jpg'
        score_threshold = '0.5'


        automl_client = automl.AutoMlClient()

        # Get the full path of the model.
        model_full_id = automl_client.model_path(
            project_id, compute_region, model_id
        )

        # Create client for prediction service.
        prediction_client = automl.PredictionServiceClient()

        # Read the image and assign to payload.
        with open(file_path, "rb") as image_file:
            content = image_file.read()
        payload = {"image": {"image_bytes": content}}

        # params is additional domain-specific parameters.
        # score_threshold is used to filter the result
        # Initialize params
        params = {}
        if score_threshold:
            params = {"score_threshold": score_threshold}

        response = prediction_client.predict(model_full_id, payload, params)
        print("Prediction results:")
        for result in response.payload:
            print("Predicted class name: {}".format(result.display_name))
            print("Predicted class score: {}".format(result.classification.score))

        # [END automl_vision_predict]

if (__name__=="__main__"):
    new_client = GCPClient()

    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    # )
    # subparsers = parser.add_subparsers(dest="command")

    # predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
    # predict_parser.add_argument("model_id")
    # predict_parser.add_argument("file_path")
    # predict_parser.add_argument("score_threshold", nargs="?", default="")

    # project_id = os.environ["PROJECT_ID"]
    # compute_region = os.environ["REGION_NAME"]

    # args = parser.parse_args()

    # if args.command == "predict":
    new_client.predict(
            # project_id,
            # compute_region,
            # args.model_id,
            # args.file_path,
            # args.score_threshold,
    )
