import boto3

class AWSClient:

    def __init__(self):
        self.rekognition = boto3.client('rekognition')
        self.s3 = boto3.resource('s3')
        self.bucket='birdviewbucket'
        self.collectionId='MyCollection'

    def put_image_on_s3(self, path, filename):
        data = open(path, 'rb')
        self.s3.Bucket('birdviewbucket').put_object(Key=filename, Body=data)

    def index_faces(self, filename):
        response = self.rekognition.index_faces(CollectionId=self.collectionId,
                                    Image={'S3Object':{'Bucket':self.bucket,
                                        'Name':filename}},
                                    ExternalImageId=filename,
                                    DetectionAttributes=['ALL'])
        faces = []
        for faceRecord in response['FaceRecords']:
             faces.append(faceRecord['Face']['FaceId'])
        return faces

    def detect_faces(self, filename):
        threshold = 70
        maxFaces=2
        response = self.rekognition.search_faces_by_image(CollectionId=self.collectionId,
                                    Image={'S3Object':{'Bucket':self.bucket,'Name':filename}},
                                    FaceMatchThreshold=threshold,
                                    MaxFaces=maxFaces)

        faceMatches=response['FaceMatches']
        print('Matching faces')
        matches = dict()
        for match in faceMatches:
            matches[match['Face']['FaceId']] = "{:.2f}".format(match['Similarity'])
            print('FaceId:' + match['Face']['FaceId'])
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print()
        return matches
