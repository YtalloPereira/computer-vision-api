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
cd grupo-6


### 2. Instalação do Serverless Framework
bash
npm install -g serverless

### 3. Configuração das Credenciais AWS

### 4. Deploy da Aplicação


## Endpoints

### Rotas Base


### Rotas de Análise


## Estrutura do Projeto

- **handler.py**: Funções Lambda para processamento das APIs.
- **serverless.yml**: Configuração do framework Serverless.
- **requirements.txt**: Dependências do projeto.

## Observações

- *Logs*: Verifique os logs no CloudWatch para depuração e validação dos resultados.

## Dificuldades Conhecidas

- *Configuração do AWS*: A configuração incorreta das credenciais pode levar a erros no deploy ou execução da função Lambda.



## Desenvolvedores


*Link do Repositório*: [https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio](https://github.com/Compass-pb-aws-2024-MAIO-A/sprint-8-pb-aws-maio) 
