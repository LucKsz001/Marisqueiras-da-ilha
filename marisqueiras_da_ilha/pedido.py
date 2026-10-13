"""Classe Pedido."""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .enums import SituacaoAnalise, StatusPedido
from .excecoes import ErroRegraNegocio, QuantidadeIndisponivelError
from .item_pedido import ItemPedido

if TYPE_CHECKING:
    from .empresa_compradora import EmpresaCompradora
    from .empresa_marisqueira import EmpresaMarisqueira
    from .produto import Produto

_proximo_id = itertools.count(1)


class Pedido:
    """Atributos: id_pedido, endereco_entrega, tempo_entrega e status_pedido.

    status_pedido: em preparo, em curso e finalizado. Ele só existe depois que a
    marisqueira aceita o pedido (antes disso é None); a fase de análise
    (aceite/rejeição/ajuste) fica em `analise`. Pagamento fora do escopo.
    """

    def __init__(self, comprador: EmpresaCompradora, endereco_entrega: str, tempo_entrega: str):
        if not endereco_entrega or not tempo_entrega:
            raise ErroRegraNegocio("Endereço e tempo de entrega são obrigatórios.")
        self.id_pedido = next(_proximo_id)
        self.comprador = comprador
        self.endereco_entrega = endereco_entrega
        self.tempo_entrega = tempo_entrega
        self.status_pedido: StatusPedido | None = None
        self.analise = SituacaoAnalise.RASCUNHO
        self.motivo_ajuste: str | None = None
        self.itens: list[ItemPedido] = []
        self.empresa_marisqueira: EmpresaMarisqueira | None = None
        self.avaliado = False

    def adicionar_item(self, produto: Produto, quantidade: float) -> ItemPedido:
        if self.analise != SituacaoAnalise.RASCUNHO:
            raise ErroRegraNegocio("Só é possível adicionar itens a um pedido em montagem.")
        # todos os produtos devem ser da mesma EMPRESA_MARISQUEIRA
        if self.empresa_marisqueira and produto.empresa is not self.empresa_marisqueira:
            raise ErroRegraNegocio("Um pedido não pode reunir produtos de empresas diferentes.")
        if any(i.produto is produto for i in self.itens):
            raise ErroRegraNegocio(f"{produto.nome} já está no pedido.")

        item = ItemPedido(self, produto, quantidade)
        item.validar_quantidade()
        if not item.verificar_disponibilidade():
            raise QuantidadeIndisponivelError(
                f"A quantidade de {quantidade} kg de {produto.nome} não está disponível "
                f"(disponível: {produto.quantidade_disponivel} kg).")

        self.itens.append(item)
        self.empresa_marisqueira = produto.empresa
        return item

    def verificar_disponibilidade(self) -> bool:
        return all(i.verificar_disponibilidade() for i in self.itens)

    @property
    def total(self) -> float:
        return sum(i.subtotal for i in self.itens)
