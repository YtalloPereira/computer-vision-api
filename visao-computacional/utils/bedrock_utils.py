import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime')

def generate_tips(pets):
    dicas = None
    if pets and pets[0]['Name'] is not None:
        pet_names = ', '.join([pet['Name'] for pet in pets if pet['Name'] is not None])
        prompt = (
            f"Generate detailed care tips for {pet_names}, including energy level information,"
            "exercise needs, temperament, behavior, care needs, and common health problems. Translate everything into Brazilian Portuguese"
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
    return dicas
