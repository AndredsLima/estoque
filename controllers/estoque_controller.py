from fastapi import APIRouter, BackgroundTasks
from service.estoque_service import EstoqueService

router = APIRouter()

@router.post("/processar")
def processar_pedido(background_tasks: BackgroundTasks):
    # Inicia o processamento de pedidos em segundo plano
    background_tasks.add_task(EstoqueService.processar_mensagens_sqs)
    return {"message": "Processamento de pedidos iniciado manualmente."}