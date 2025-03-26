from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, JSON
from config.database import Base

class ItemDTO(BaseModel):
    produtoId: int
    quantidade: int

    def dict(self, **kwargs):
        return super().dict(**kwargs)

class PedidoDTO(BaseModel):
    id: int
    cliente: str
    itens: List[ItemDTO]

class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    itens = Column(JSON, nullable=False)  # Armazena os itens como JSON