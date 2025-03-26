🛒 Sistema de Estoque com FastAPI e LocalStack
📋 Requisitos
Docker 

Python 3.8+

🚀 Como Executar
1. Iniciar os Containers (PostgreSQL + LocalStack)

docker-compose up -d

2. Criar a Fila SQS (LocalStack)
Execute apenas uma vez:
docker exec -it estoque-localstack-1 awslocal sqs create-queue --queue-name fila-pedidos

3. Instalar Dependências

pip install -r requirements.txt

4. Iniciar a API (FastAPI)

uvicorn main:app --reload