"""Classe EmpresaCompradora."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .avaliacao import Avaliacao
from .enums import Categoria, StatusPedido
from .excecoes import ErroRegraNegocio
from .pedido import Pedido
from .validacao import validar_cnpj

if TYPE_CHECKING:
    from .empresa_marisqueira import EmpresaMarisqueira
    from .produto import Produto


class EmpresaCompradora:
    """Empresa que realiza as compras.

    Atributos: id_empresa_compradora (CNPJ), nome e localizacao.
    """

    def __init__(self, id_empresa_compradora: str, nome: str, localizacao: str):
        if not nome or not localizacao:
            raise ErroRegraNegocio("Nome e localização da empresa são obrigatórios.")
        self.id_empresa_compradora = validar_cnpj(id_empresa_compradora)
        self.nome = nome
        self.localizacao = localizacao  # critério de consulta; guardada como texto
        self.pedidos: list[Pedido] = []

    def consultar_produtos(self, marisqueiras: list[EmpresaMarisqueira], nome: str | None = None,
                           categoria: Categoria | None = None, localizacao: str | None = None,
                           empresa: str | None = None, avaliacao_minima: float | None = None,
                           ordenar_por: str | None = None) -> list[Produto]:
        """RN10/RN11. ordenar_por: 'menor_preco' | 'maior_preco' | 'melhor_avaliacao' | 'proximidade'.
        Produtos indisponíveis continuam aparecendo (RN09)."""
        resultado = [p for m in marisqueiras for p in m.produtos]

        if nome:
            resultado = [p for p in resultado if nome.lower() in p.nome.lower()]
        if categoria:
            resultado = [p for p in resultado if p.categoria == categoria]
        if localizacao:
            resultado = [p for p in resultado if localizacao.lower() in p.empresa.localizacao.lower()]
        if empresa:
            resultado = [p for p in resultado if empresa.lower() in p.empresa.nome.lower()]
        if avaliacao_minima is not None:
            resultado = [p for p in resultado if p.empresa.media_avaliacoes >= avaliacao_minima]

        ordenacoes = {
            "menor_preco": lambda p: p.preco,
            "maior_preco": lambda p: -p.preco,
            "melhor_avaliacao": lambda p: -p.empresa.media_avaliacoes,
            # sem coordenadas: mesma localização da compradora vem primeiro
            "proximidade": lambda p: (p.empresa.localizacao != self.localizacao, p.empresa.localizacao),
        }
        if ordenar_por:
            if ordenar_por not in ordenacoes:
                raise ErroRegraNegocio(f"Ordenação inválida. Use: {', '.join(ordenacoes)}.")
            resultado.sort(key=ordenacoes[ordenar_por])
        return resultado

    def comparar_produtos(self, produtos: list[Produto]) -> list[dict]:
        """Compara produtos de empresas diferentes (ordenados pelo menor preço)."""
        if len(produtos) < 2:
            raise ErroRegraNegocio("Selecione ao menos 2 produtos para comparar.")
        return [
            {
                "produto": p.nome,
                "categoria": p.categoria.value,
                "empresa": p.empresa.nome,
                "preco": p.preco,
                "disponivel_kg": p.quantidade_disponivel,
                "avaliacao": round(p.empresa.media_avaliacoes, 1),
                "localizacao": p.empresa.localizacao,
            }
            for p in sorted(produtos, key=lambda p: p.preco)
        ]

    def realizar_pedido(self, itens: list[tuple[Produto, float]], endereco_entrega: str,
                        tempo_entrega: str) -> Pedido:
        """itens = [(produto, quantidade_kg), ...]"""
        if not itens:
            raise ErroRegraNegocio("O pedido deve ter ao menos um produto.")
        pedido = Pedido(self, endereco_entrega, tempo_entrega)
        for produto, quantidade in itens:
            pedido.adicionar_item(produto, quantidade)  # valida mínimo, estoque e empresa única
        pedido.empresa_marisqueira.receber_pedido(pedido)
        self.pedidos.append(pedido)
        return pedido

    def avaliar_empresa(self, pedido: Pedido, nota: int) -> Avaliacao:
        """Só após a compra (pedido finalizado), uma vez por pedido."""
        if pedido not in self.pedidos:
            raise ErroRegraNegocio("Este pedido não pertence a esta empresa compradora.")
        if pedido.status_pedido != StatusPedido.FINALIZADO:
            raise ErroRegraNegocio("A avaliação só pode ser feita após o pedido ser finalizado.")
        if pedido.avaliado:
            raise ErroRegraNegocio("Este pedido já foi avaliado.")
        avaliacao = Avaliacao(self, pedido.empresa_marisqueira, pedido)
        avaliacao.registrar_nota(nota)
        pedido.avaliado = True
        return avaliacao

    def __repr__(self) -> str:
        return f"EmpresaCompradora({self.nome!r})"
