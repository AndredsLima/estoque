from sqlalchemy.orm import Session
from models.pedido_models import PedidoDB

class EstoqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar_pedido(self, pedido):
        db_pedido = PedidoDB(cliente=pedido.cliente, itens=pedido.itens)
        self.db.add(db_pedido)
        self.db.commit()
        self.db.refresh(db_pedido)
        return db_pedido