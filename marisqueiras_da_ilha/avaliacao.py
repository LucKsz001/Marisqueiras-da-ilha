"""Classe Avaliacao."""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .excecoes import ErroRegraNegocio

if TYPE_CHECKING:
    from .empresa_compradora import EmpresaCompradora
    from .empresa_marisqueira import EmpresaMarisqueira
    from .pedido import Pedido

_proximo_id = itertools.count(1)


class Avaliacao:
    """Atributos: id_avaliacao e nota (1 a 5 estrelas).

    O documento não define a cardinalidade exata; decisão de modelagem: uma avaliação
    por pedido, feita pela compradora para a marisqueira do pedido.
    """

    def __init__(self, comprador: EmpresaCompradora, empresa: EmpresaMarisqueira, pedido: Pedido):
        self.id_avaliacao = next(_proximo_id)
        self.comprador = comprador
        self.empresa = empresa
        self.pedido = pedido
        self.nota: int | None = None

    def registrar_nota(self, nota: int) -> None:
        if isinstance(nota, bool) or not isinstance(nota, int) or not 1 <= nota <= 5:
            raise ErroRegraNegocio("A nota deve ser um número inteiro de 1 a 5 estrelas.")
        self.nota = nota
        self.empresa.avaliacoes.append(self)
