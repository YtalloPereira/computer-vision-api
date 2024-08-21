import json
import boto3
from datetime import datetime

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime')



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
        
        # Obter o horário atual
        created_image_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

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
                "created_image": created_image_time,
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
                "created_image": created_image_time,
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

        # Obter a data de criação do objeto no S3
        s3_response = s3.head_object(Bucket=bucket, Key=image_name)
        created_image_time = s3_response['LastModified'].strftime("%d-%m-%Y %H:%M:%S")

        # Detectar faces
        rekognition_faces_response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            Attributes=['ALL']
        )

        print(rekognition_faces_response)

        # Detectar pets
        rekognition_labels_response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            MaxLabels=10,
            MinConfidence=90
        )

        print(rekognition_labels_response)

        # Processamento das faces detectadas
        faces = []
        for faceDetail in rekognition_faces_response['FaceDetails']:
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

        # Se nenhuma face foi detectada, adicionar valores None
        if not faces:
            faces.append({
                "position": {
                    "Height": None,
                    "Left": None,
                    "Top": None,
                    "Width": None
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None
            })

        # Processameto os pets detectados
        pets = []
        for label in rekognition_labels_response['Labels']:
            pets.append({
                "Confidence": label['Confidence'],
                "Name": label['Name']
            })
        
        # nenhum pet foi detectado, adicionar valores None
        if not pets:
            pets.append({
                "Confidence": None,
                "Name": None
            })
        
        # Gerando dicas
        dicas = None
        if pets and pets[0]['Name'] is not None:
            pet_names = ', '.join([pet['Name'] for pet in pets if pet['Name'] is not None])
            prompt = (
                f"Gerar dicas detalhadas sobre cuidados para {pet_names}, incluindo informações sobre nível de energia, "
                "necessidades de exercícios, temperamento, comportamento, cuidados necessários, e problemas de saúde comuns."
            )

            native_request = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 512,
                    "temperature": 0.9,
                },
            }

            try:
                bedrock_response = bedrock_runtime.invoke_model(
                    modelId='amazon.titan-text-premier-v1:0',
                    body=json.dumps(native_request),
                    contentType='application/json'
                )

                response_body = json.loads(bedrock_response['body'].read())
                dicas = response_body['results'][0]['outputText']
            except Exception as e:
                dicas = f"Erro ao gerar dicas: {str(e)}"

        # Montar a resposta
        response_body = {
            "url_to_image": f"https://{bucket}.s3.amazonaws.com/{image_name}",
            "created_image": created_image_time,
            "faces": faces,
            "pets": pets,
            "Dicas": dicas
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
