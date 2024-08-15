import json


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

        # Adicionar lógica para chamada ao Rekognition e processamento da resposta;
        # obter a lista de faces detectadas; lógica para processar o Rekognition e preencher a lista `faces.

        faces = [] 


        if not faces:
            response_body = {
                "url_to_image": f"https://{bucket}/{image_name}",
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
                "url_to_image": f"https://{bucket}/{image_name}",
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
