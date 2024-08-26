import boto3

rekognition = boto3.client('rekognition')

def detect_faces(bucket, image_name):
    response = rekognition.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
        Attributes=['ALL']
    )
    return response['FaceDetails']

def detect_labels(bucket, image_name):
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
        MaxLabels=10,
        MinConfidence=90
    )
    return response['Labels']
