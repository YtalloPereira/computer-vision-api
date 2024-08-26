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
git clone https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio.git
git checkout grupo-6


### 2. Instalação do Serverless Framework

npm install -g serverless

### 3. Configuração das Credenciais AWS

Configure suas credenciais AWS. Você pode usar o Serverless Framework ou a AWS CLI.

**Usando Serverless Framework:**
```bash
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Usando AWS CLI:**
```bash
aws configure
```

### 4. Deploy da Aplicação

Para implantar a aplicação na AWS, execute:
```bash
serverless deploy
```

Após o deploy, você verá os endpoints gerados e outros detalhes importantes.

## Endpoints

### Rotas Base

- **GET /**: Retorna uma mensagem de confirmação de que a função Lambda está funcionando.
  - **Resposta Esperada:**
    ```json
    { 
      "message": "Go Serverless v3.0! Your function executed successfully!", 
      "input": { ... }
    }
    ```
  - **Status Code**: 200

- **GET /v1**: Retorna uma mensagem de versão da API.
  - **Resposta Esperada:**
    ```json
    { "message": "VISION api version 1." }
    ```
  - **Status Code**: 200

- **GET /v2**: Retorna uma mensagem de versão da API.
  - **Resposta Esperada:**
    ```json
    { "message": "VISION api version 2." }
    ```
  - **Status Code**: 200

### Rotas de Análise

- **POST /v1/vision**: Analisa a emoção das faces em uma imagem.
  - **Formato de Entrada:**
    ```json
    { 
      "bucket": "myphotos", 
      "imageName": "test-happy.jpg" 
    }
    ```
  - **Formato de Saída:**
    ```json
    { 
      "url_to_image": "https://myphotos/test.jpg", 
      "created_image": "02-02-2023 17:00:00", 
      "faces": [ 
        { 
          "position": { "Height": 0.063, "Left": 0.171, "Top": 0.737, "Width": 0.111 },
          "classified_emotion": "HAPPY", 
          "classified_emotion_confidence": 99.93 
        } 
      ] 
    }
    ```
  - **Status Code**: 200

- **POST /v2/vision**: Analisa emoções e verifica a presença de pets em uma imagem.
  - **Formato de Entrada:**
    ```json
    {  
      "bucket": "myphotos",  
      "imageName": "labrador.jpg"  
    }
    ```
  - **Formato de Saída:**
    ```json
    {  
      "url_to_image": "https://mycatphotos/cat.jpg",  
      "created_image": "02-02-2023 17:00:00",  
      "pets": [
        {
          "labels": [  
            { "Confidence": 96.59, "Name": "Animal" },  
            { "Confidence": 96.59, "Name": "Dog" },  
            { "Confidence": 96.59, "Name": "Pet" },  
            { "Confidence": 96.59, "Name": "Labrador" }  
          ],  
          "Dicas": "Dicas sobre Labradores: Nível de Energia e Necessidades de Exercícios: Labradores são de médio nível de energia, necessitando de 40 minutos de exercício por dia. Temperamento e Comportamento: Inteligentes, enérgicos, dóceis, e com forte desejo de trabalhar com pessoas. Cuidados e Necessidades: Pelos curtos que precisam de poucos cuidados, mas devem ser penteados uma vez por semana para remover fios mortos e soltos. A alimentação deve ser adequada, ajustando a quantidade conforme o peso do cão. Problemas de Saúde Comuns: Displasia do cotovelo e coxofemoral, atrofia progressiva da retina (APR) e catarata hereditária." 
        }
      ]
    }
    ```
  - **Status Code**: 200


## Estrutura do Projeto

- **handler.py**: Funções Lambda para processamento das APIs.
- **serverless.yml**: Configuração do framework Serverless.
- **requirements.txt**: Dependências do projeto.

## Observações

- *Logs*: Verifique os logs no CloudWatch para depuração e validação dos resultados.

## Dificuldades Conhecidas

- *Configuração do AWS*: A configuração incorreta das credenciais pode levar a erros no deploy ou execução da função Lambda.



## Desenvolvedores

- José Luan
- Ytollo Pereira
- Ygor Silva
- Naira Miriam
