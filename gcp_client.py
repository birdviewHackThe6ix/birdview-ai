# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

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
    
