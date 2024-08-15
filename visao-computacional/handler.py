import json
import boto3


rekognition = boto3.client('rekognition')


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "VISION api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v2_description(event, context):
    body = {
        "message": "VISION api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def face_emotion_analysis_v1(event, context):
    try:
        body = json.loads(event['body'])
        bucket = body.get('bucket')
        image_name = body.get('imageName')

        # Construir a URL da imagem no formato padrão do S3
        image_url = f"https://{bucket}.s3.amazonaws.com/{image_name}"

        # Chamada ao Rekognition para detectar faces na imagem
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            Attributes=['ALL']
        )

        # Log da resposta do Rekognition
        print(response)

        faces = []

        for faceDetail in response['FaceDetails']:
            faces.append({
                "position": {
                    "Height": faceDetail['BoundingBox']['Height'],
                    "Left": faceDetail['BoundingBox']['Left'],
                    "Top": faceDetail['BoundingBox']['Top'],
                    "Width": faceDetail['BoundingBox']['Width']
                },
                "classified_emotion": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Type'],
                "classified_emotion_confidence": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Confidence']
            })

        if not faces:
            response_body = {
                "url_to_image": image_url,
                "created_image": "02-02-2023 17:00:00",
                "faces": [
                    {
                        "position": {
                            "Height": None, # não alterar parar null
                            "Left": None,   # a função dumps converte
                            "Top": None,
                            "Width": None
                        },
                        "classified_emotion": None,
                        "classified_emotion_confidence": None
                    }
                ]
            }
        else:
            response_body = {
                "url_to_image": image_url,
                "created_image": "02-02-2023 17:00:00",
                "faces": faces  # lista de faces detectadas
            }

        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Erro ao processar a solicitação.",
                    "error": str(e)
                }
            )
        }

    return response

def face_and_pet_analysis_v2(event, context):
    try:
        body = json.loads(event['body'])
        bucket = body.get('bucket')
        image_name = body.get('imageName')

        # Adicionar lógica para chamada ao Rekognition para detectar pets e faces;
        # Processar a resposta do Rekognition e preencher a lista `faces` e `pets`.
        
        faces = []  # Lista de faces detectadas
        pets = []   # Lista de pets detectados

        # exemplo do readme do projeto
        if not faces and not pets:
            response_body = {
                "url_to_image": f"https://{bucket}/{image_name}",
                "created_image": "02-02-2023 17:00:00",
                "faces": [
                    {
                        "position": {
                            "Height": None,
                            "Left": None,
                            "Top": None,
                            "Width": None
                        },
                        "classified_emotion": None,
                        "classified_emotion_confidence": None
                    }
                ],
                "pets": []
            }
        else:
            response_body = {
                "url_to_image": f"https://{bucket}/{image_name}",
                "created_image": "02-02-2023 17:00:00",
                "faces": faces,
                "pets": pets
            }

        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Erro ao processar a solicitação.",
                    "error": str(e)
                }
            )
        }

    return response
