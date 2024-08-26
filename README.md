# Face & Pet Analyzer API
Uma API que utiliza o Amazon Rekognition e Bedrock para analisar faces e identificar animais de estimação em imagens (cachorros, gatos e pássaros).

## Funcionalidades
Análise de Emoções Faciais (v1):

    Detecta rostos em uma imagem armazenada no Amazon S3.
    Identifica e classifica a emoção dominante em cada rosto detectado.
    Retorna a posição dos rostos na imagem e a emoção classificada com seu nível de confiança.

Análise de Emoções Faciais e Detecção de Animais (v2):

    Detecta rostos e animais de estimação em uma imagem armazenada no Amazon S3.
    Identifica a emoção dominante em cada rosto detectado.
    Retorna a posição dos rostos, a emoção classificada, e os animais detectados na imagem.
    Gera dicas de cuidados para os animais detectados usando o Amazon Bedrock.

## Configuração do Projeto

### 1. Clonando o Repositório
Clone o repositório do projeto para o seu ambiente local usando o comando
 bash
git clone https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio



### 2. Instalação do Serverless Framework
no terminal, utilize o comando
npm install -g serverless

### 3. Configuração das Credenciais AWS

```bash 
serverless config credentials \ 
   --provider aws \ 
   --key AKIAIOSFODNN7EXAMPLE \ 
   --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY 
``` 
### 4. Criação do arquivo '.env'

Após configurar as credenciais da AWS, crie um arquivo .env na pasta raiz do projeto. Este arquivo será usado para armazenar as variáveis de ambiente necessárias para o funcionamento da aplicação.

No terminal, execute:
```bash
touch visao-computacional/.env
``` 
Abra o arquivo .env em um editor de texto e adicione as seguintes variáveis:

```bash
REGION= #Região de onde deverá ser feito o deploy
BUCKET_NAME= #Nome da Bucket que contém as imagens que serão utilizadas
APP_NAME= #Nome do app no serverless
ORG_NAME= #Nome da Org do serverless
``` 


### 4. Deploy da Aplicação

Para efetuar o deploy da solução na sua conta aws execute (acesse a pasta [visao-computacional](./visao-computacional) ):
  
```bash
serverless deploy 
```
  
Depois de efetuar o deploy, vocẽ terá um retorno parecido com isso: 
  
```bash

DOTENV: Loading environment variables from .env:

         - REGION

         - BUCKET_NAME

         - APP_NAME

         - ORG_NAME

Deploying "vision" to stage "dev" (us-east-1)

[!] Function (faceAndPetAnalysisV2) timeout setting (30) may not provide enough room to process an HTTP API request (of which timeout is limited to 30s). This may introduce a situation where endpoint times out for a successful lambda invocation.

✔ Service deployed to stack vision-dev (54s)

endpoints:
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1/vision
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2/vision
functions:
  health: vision-dev-health (44 MB)
  v1Description: vision-dev-v1Description (44 MB)
  v2Description: vision-dev-v2Description (44 MB)
  faceEmotionAnalysisV1: vision-dev-faceEmotionAnalysisV1 (44 MB)
  faceAndPetAnalysisV2: vision-dev-faceAndPetAnalysisV2 (44 MB)
```

## Endpoints



## Estrutura do Projeto
```bash
/SPRINT-8-PB-AWS-MAIO/
│
├── assets/
│   └── arquitetura-base.jpg
├── visao-computacional/
│   ├── handlers/
│   │   ├── health_handler.py
│   │   ├── description_handler.py
│   │   └── analysis_handler.py
│   ├── utils/
│   │   ├── bedrock_utils.py
│   │   ├── rekognition_utils.py
│   │   └── s3_utils.py
│   ├── .env
│   ├── .gitignore
│   └── serverless.yml
├── .gitignore
└── README.md

```

### 5. Rotas Disponíveis

Após o deploy, as seguintes rotas estarão disponíveis:

- **GET /**: Verifica a saúde da aplicação.
  
  **Exemplo de resposta:**
  ```json
  {
    "message": "Go Serverless v3.0! Your function executed successfully!",
    "input": {...input}
  }
- **GET /v1**: Descrição da versão 1 da API.

   **Exemplo de resposta:**
   ```json
   {
      "message": "VISION api version 1."
   }
- **GET /v2**: Descrição da versão 2 da API.

   **Exemplo de resposta:**
   ```json
   {
      "message": "VISION api version 2."
   }

- **POST /v1/vision**: Análise de emoções faciais em uma imagem.

   **Requerimentos:**
   ```json
   {
      "bucket": "nome-do-bucket",
      "imageName": "nome-da-imagem"
   }
   ```
   **Exemplo de resposta:**
   ```json
   {
      "url_to_image": "https://nome-do-bucket.s3.amazonaws.com/nome-da-imagem",
      "created_image": "dd-mm-yyyy hh:mm:ss",
      "faces": [
         {
            "position": {
            "Height": 0.5,
            "Left": 0.3,
            "Top": 0.2,
            "Width": 0.4
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 99.9
         }
      ]
   }
   ```

- **POST /v2/vision**: Análise de emoções faciais e detecção de pets em uma imagem, com geração de dicas.

   **Requerimentos:**
   ```json
   {
      "bucket": "nome-do-bucket",
      "imageName": "nome-da-imagem"
   }
   ```
   **Exemplo de resposta:**
   ```json
   {
      "url_to_image": "https://nome-do-bucket.s3.amazonaws.com/nome-da-imagem",
      "created_image": "data-e-hora-de-criação",
      "faces": [
            {
               "position": {
                  "Height": 0.1,
                  "Left": 0.5,
                  "Top": 0.2,
                  "Width": 0.3
               },
               "classified_emotion": "HAPPY",
               "classified_emotion_confidence": 99.9
            }
         ],
      "pets": [
            {
               "Confidence": 98.5,
               "Name": "Cat"
            }
         ],
      "Dicas": "Aqui vão as dicas detalhadas sobre cuidados com o pet..."
      }

   ```
   



## Observações

- *Logs*: Verifique os logs no CloudWatch para depuração e validação dos resultados.


## Dificuldades Conhecidas
- *Configuração do serverless*
- *Configuração do AWS*: A configuração incorreta das credenciais pode levar a erros no deploy ou execução da função Lambda.
- *Filtro de labels*: filtrar as labels referentes a animais
- *configurações do prompt do Bedrock*



## Desenvolvedores
## 👥 Desenvolvedores

- **[Ygor Silva](https://github.com/Ygor-Matos)**
- **[Luan Fernandes](https://github.com/https-Luan-Fernandes)**
- **[Naira Miriam](https://github.com/NairaMiriam02)**
- **[Ytallo Pereira](https://github.com/YtalloPereira)**

*Link do Repositório*: [https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio](https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio) 