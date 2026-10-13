"""Classe Produto."""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .constantes import QUANTIDADE_MINIMA_KG
from .enums import Categoria
from .excecoes import ErroRegraNegocio

if TYPE_CHECKING:
    from .empresa_marisqueira import EmpresaMarisqueira

_proximo_id = itertools.count(1)


class Produto:
    """Atributos: id_produto, nome, categoria, preco, quantidade_disponivel (kg), fotografia (opcional).

    Fresco e congelado são produtos diferentes (RN06). Com quantidade zero, o produto
    permanece cadastrado e aparece como indisponível (RN09).
    """

    def __init__(self, empresa: EmpresaMarisqueira, nome: str, categoria: Categoria,
                 preco: float, quantidade_disponivel: float, fotografia: str | None = None):
        if not nome or not isinstance(categoria, Categoria) or preco is None or quantidade_disponivel is None:
            raise ErroRegraNegocio("Todos os dados do produto são obrigatórios, exceto a fotografia.")
        if preco <= 0:
            raise ErroRegraNegocio("O preço deve ser maior que zero.")
        if quantidade_disponivel < QUANTIDADE_MINIMA_KG:  # P19
            raise ErroRegraNegocio(
                f"A quantidade disponível informada deve atender ao mínimo de {QUANTIDADE_MINIMA_KG} kg.")
        self.id_produto = next(_proximo_id)
        self.empresa = empresa
        self.nome = nome
        self.categoria = categoria
        self.preco = preco  # RN07: definido por produto e empresa
        self.quantidade_disponivel = quantidade_disponivel
        self.fotografia = fotografia

    def verificar_disponibilidade(self, quantidade: float = QUANTIDADE_MINIMA_KG) -> bool:
        """True se há estoque suficiente para a quantidade pedida (RN17/RN18)."""
        return self.quantidade_disponivel >= quantidade

    def atualizar_quantidade(self, nova_quantidade: float) -> None:
        """Define a nova quantidade disponível (RN08). Zero = indisponível (RN09)."""
        if nova_quantidade < 0:
            raise ErroRegraNegocio("A quantidade disponível não pode ser negativa.")
        self.quantidade_disponivel = nova_quantidade

    @property
    def indisponivel(self) -> bool:
        return self.quantidade_disponivel <= 0

    def __repr__(self) -> str:
        return (f"Produto({self.nome!r}, {self.categoria.value}, "
                f"R${self.preco:.2f}/kg, {self.quantidade_disponivel}kg)")
