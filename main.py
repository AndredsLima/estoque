from fastapi import FastAPI
from service.estoque_service import EstoqueService
import threading
import logging
from config.database import criar_tabelas

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Cria as tabelas no banco de dados
criar_tabelas()
logger.info("Tabelas do banco de dados criadas com sucesso.")

def start_polling():
    """Função que inicia a verificação da fila SQS em segundo plano"""
    logger.info("Iniciando thread de verificação da fila SQS...")
    EstoqueService.start_polling(interval=10)  # Usando o novo nome da função

# Inicia a thread em segundo plano
threading.Thread(target=start_polling, daemon=True).start()