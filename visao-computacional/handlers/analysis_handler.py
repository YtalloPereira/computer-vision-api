import json
from utils.s3_utils import get_s3_image_info
from utils.rekognition_utils import detect_faces, detect_labels
from utils.bedrock_utils import generate_tips

# Função para análise de emoções faciais em imagens
def face_emotion_analysis_v1(event, context):
    try:
        # Extrai informações do corpo da solicitação (JSON) enviada ao Lambda
        body = json.loads(event['body'])
        bucket = body.get('bucket')  # Nome do bucket S3
        image_name = body.get('imageName')  # Nome da imagem no S3

        # Obtém a hora de criação e a URL da imagem no S3
        created_image_time, image_url = get_s3_image_info(bucket, image_name)

        # Detecta rostos na imagem usando Amazon Rekognition
        face_details = detect_faces(bucket, image_name)

        faces = []
        # Itera sobre os detalhes dos rostos detectados
        for faceDetail in face_details:
            # Adiciona as informações do rosto à lista 'faces', incluindo posição e emoção classificada
            faces.append({
                "position": {
                    "Height": faceDetail['BoundingBox']['Height'],  # Altura do rosto
                    "Left": faceDetail['BoundingBox']['Left'],  # Posição à esquerda
                    "Top": faceDetail['BoundingBox']['Top'],  # Posição superior
                    "Width": faceDetail['BoundingBox']['Width']  # Largura do rosto
                },
                # Emotions retorna uma lista de emoções com suas respectivas confidências.
                # Aqui, selecionamos a emoção com a maior confiança.
                "classified_emotion": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Type'],
                "classified_emotion_confidence": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Confidence']
            })

        # Caso nenhum rosto seja detectado, adiciona uma entrada nula na lista 'faces'
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

        # Monta o corpo da resposta com as informações da imagem e dos rostos detectados
        response_body = {
            "url_to_image": image_url,
            "created_image": created_image_time,
            "faces": faces
        }

        # Retorna a resposta com status 200 (sucesso) e o corpo da resposta em JSON
        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }
    except Exception as e:
        # Em caso de erro, retorna uma resposta com status 500 (erro interno) e a mensagem de erro
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

# Função para análise de emoções faciais e detecção de pets em imagens
def face_and_pet_analysis_v2(event, context):
    try:
        # Extrai informações do corpo da solicitação (JSON) enviada ao Lambda
        body = json.loads(event['body'])
        bucket = body.get('bucket')  # Nome do bucket S3
        image_name = body.get('imageName')  # Nome da imagem no S3

        # Obtém a hora de criação e a URL da imagem no S3
        created_image_time, image_url = get_s3_image_info(bucket, image_name)

        # Detecta rostos na imagem usando Amazon Rekognition
        face_details = detect_faces(bucket, image_name)
        
        # Detecta rótulos na imagem usando Amazon Rekognition, o que pode incluir pets
        pet_labels = detect_labels(bucket, image_name)

        faces = []
        # Itera sobre os detalhes dos rostos detectados
        for faceDetail in face_details:
            # Adiciona as informações do rosto à lista 'faces', incluindo posição e emoção classificada
            faces.append({
                "position": {
                    "Height": faceDetail['BoundingBox']['Height'],  # Altura do rosto
                    "Left": faceDetail['BoundingBox']['Left'],  # Posição à esquerda
                    "Top": faceDetail['BoundingBox']['Top'],  # Posição superior
                    "Width": faceDetail['BoundingBox']['Width']  # Largura do rosto
                },
                # Emotions retorna uma lista de emoções com suas respectivas confidências.
                # Aqui, selecionamos a emoção com a maior confiança.
                "classified_emotion": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Type'],
                "classified_emotion_confidence": max(faceDetail['Emotions'], key=lambda e: e['Confidence'])['Confidence']
            })

        # Caso nenhum rosto seja detectado, adiciona uma entrada nula na lista 'faces'
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

        # Lista de raças de cães, tipos de gatos e pássaros que o Rekognition pode detectar
        pet_labels_of_interest = [
            # Raças de Cães
            "Dog", "Beagle", "Bulldog", "Chihuahua", "Dalmatian", "Golden Retriever",
            "Great Dane", "Labrador Retriever", "Poodle", "Pug", "Shih Tzu",
            "Siberian Husky", "Yorkshire Terrier", "Boxer", "Dachshund", 
            "German Shepherd", "Rottweiler", "Border Collie", "Maltese", 
            "Cocker Spaniel", "Basset Hound",
            # Tipos de Gatos
            "Cat",
            # Tipos de Pássaros
            "Bird", "Sparrow", "Parrot", "Canary", "Owl", "Eagle", "Hawk",
            "Pigeon", "Crow", "Peacock", "Penguin", "Flamingo", "Duck", "Swan", "Arara"
        ]

        pets = []
        # Itera sobre os rótulos detectados e filtra aqueles de interesse
        for label in pet_labels:
            if label['Name'] in pet_labels_of_interest:
                # Adiciona o rótulo à lista 'pets' se estiver na lista de interesse
                pets.append({
                    "Confidence": label['Confidence'],  # Confiança da detecção
                    "Name": label['Name']  # Nome do rótulo (ex: raça do cão, tipo de pássaro)
                })

        # Caso nenhum pet de interesse seja detectado, adiciona uma entrada nula na lista 'pets'
        if not pets:
            pets.append({
                "Confidence": None,
                "Name": None
            })

        # Gera dicas com base nos pets detectados usando a função `generate_tips`
        dicas = generate_tips(pets)

        # Monta o corpo da resposta com as informações da imagem, dos rostos e dos pets detectados
        response_body = {
            "url_to_image": image_url,
            "created_image": created_image_time,
            "faces": faces,
            "pets": pets,
            "Dicas": dicas
        }

        # Retorna a resposta com status 200 (sucesso) e o corpo da resposta em JSON
        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        # Em caso de erro, retorna uma resposta com status 500 (erro interno) e a mensagem de erro
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
