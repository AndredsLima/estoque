import time
import json
import logging
from config.sqs_config import sqs, queue_url
from repository.estoque_repository import EstoqueRepository
from models.pedido_models import PedidoDTO
from config.database import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class EstoqueService:
    @staticmethod
    def process_order(pedido_data):
        """Processa um pedido da fila SQS"""
        db = SessionLocal()
        try:
            pedido = PedidoDTO(**pedido_data)
            logger.info(f"Processando pedido: {pedido}")

            itens_dict = [item.dict() for item in pedido.itens]
            pedido.itens = itens_dict

            repository = EstoqueRepository(db)
            repository.salvar_pedido(pedido)
            logger.info("Pedido salvo no banco com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao processar pedido: {e}")
        finally:
            db.close()

    @staticmethod
    def delete_message(receipt_handle):
        """Remove mensagem da fila SQS"""
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        logger.info("Mensagem removida da fila.")

    @staticmethod
    def process_message(message):
        """Processa uma mensagem da fila"""
        try:
            pedido_data = json.loads(message['Body'])
            EstoqueService.process_order(pedido_data)
            EstoqueService.delete_message(message['ReceiptHandle'])
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")

    @staticmethod
    def check_queue():
        """Verifica a fila por mensagens"""
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=0
            )
            return response.get('Messages', [])
        except Exception as e:
            logger.error(f"Erro ao verificar fila: {e}")
            return []

    @staticmethod
    def start_polling(interval=10, max_attempts=10):
        """Inicia o serviço de verificação da fila"""
        logger.info("Iniciando verificação da fila SQS...")

        for attempt in range(max_attempts):
            logger.info(f"Tentativa {attempt + 1}/{max_attempts}")

            messages = EstoqueService.check_queue()
            if messages:
                EstoqueService.process_message(messages[0])
                return

            time.sleep(interval)

        logger.info("Máximo de tentativas alcançado.")