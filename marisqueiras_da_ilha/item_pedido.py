"""Classe ItemPedido (entidade associativa entre Pedido e Produto)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .constantes import QUANTIDADE_MINIMA_KG
from .excecoes import ErroRegraNegocio

if TYPE_CHECKING:
    from .pedido import Pedido
    from .produto import Produto


class ItemPedido:
    """Atributos: id_pedido, id_produto e quantidade (kg)."""

    def __init__(self, pedido: Pedido, produto: Produto, quantidade: float):
        self.pedido = pedido
        self.produto = produto
        self.quantidade = quantidade
        # RN07: o preço fica "congelado" no pedido e não muda durante a venda
        self.preco_unitario = produto.preco

    @property
    def id_pedido(self) -> int:
        return self.pedido.id_pedido

    @property
    def id_produto(self) -> int:
        return self.produto.id_produto

    def validar_quantidade(self) -> None:
        """RN05/RN15: mínimo de 25 kg por produto. RN16: não há valor mínimo em dinheiro."""
        if self.quantidade < QUANTIDADE_MINIMA_KG:
            raise ErroRegraNegocio(
                f"Quantidade mínima de {QUANTIDADE_MINIMA_KG} kg por produto "
                f"({self.produto.nome}: {self.quantidade} kg).")

    def verificar_disponibilidade(self) -> bool:
        """RN17/RN18: a quantidade solicitada não pode ultrapassar o estoque."""
        return self.produto.verificar_disponibilidade(self.quantidade)

    @property
    def subtotal(self) -> float:
        # RN23: custo da entrega já incorporado ao preço
        return self.quantidade * self.preco_unitario
