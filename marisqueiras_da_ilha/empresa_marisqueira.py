"""Classe EmpresaMarisqueira."""
from __future__ import annotations

from datetime import datetime, time
from typing import TYPE_CHECKING

from .constantes import LIMITE_ESTOQUE_BAIXO_KG
from .enums import Categoria, SituacaoAnalise, SituacaoEmpresa, StatusPedido
from .excecoes import ErroRegraNegocio, QuantidadeIndisponivelError
from .produto import Produto
from .validacao import validar_cnpj

if TYPE_CHECKING:
    from .avaliacao import Avaliacao
    from .pedido import Pedido

# sequência obrigatória do status_pedido
_ORDEM_STATUS = [StatusPedido.EM_PREPARO, StatusPedido.EM_CURSO, StatusPedido.FINALIZADO]


class EmpresaMarisqueira:
    """Empresa responsável pelo fornecimento dos produtos e pela entrega.

    Atributos: id_empresa_marisqueira (CNPJ), nome e localizacao.
    `abertura`/`fechamento` são extras de implementação, necessários para o
    indicador "fora do horário de funcionamento" (RN20).
    """

    def __init__(self, id_empresa_marisqueira: str, nome: str, localizacao: str,
                 abertura: time = time(6, 0), fechamento: time = time(18, 0)):
        if not nome or not localizacao:
            raise ErroRegraNegocio("Nome e localização da empresa são obrigatórios.")
        self.id_empresa_marisqueira = validar_cnpj(id_empresa_marisqueira)
        self.nome = nome
        self.localizacao = localizacao  # critério de consulta; guardada como texto
        self.abertura = abertura
        self.fechamento = fechamento
        self.produtos: list[Produto] = []
        self.pedidos_recebidos: list[Pedido] = []
        self.avaliacoes: list[Avaliacao] = []

    # --- produtos / estoque ---
    def cadastrar_produto(self, nome: str, categoria: Categoria, preco: float,
                          quantidade_disponivel: float, fotografia: str | None = None) -> Produto:
        # RN06: fresco e congelado são produtos diferentes
        if any(p.nome.lower() == str(nome).lower() and p.categoria == categoria for p in self.produtos):
            raise ErroRegraNegocio(f"{nome} já está cadastrado nessa categoria.")
        produto = Produto(self, nome, categoria, preco, quantidade_disponivel, fotografia)
        self.produtos.append(produto)
        return produto

    def alterar_quantidade(self, produto: Produto, nova_quantidade: float) -> None:
        """RN08: a pessoa responsável pode alterar a qualquer momento."""
        if produto not in self.produtos:  # RN12: só mexe nos próprios produtos
            raise ErroRegraNegocio("A empresa só pode alterar seus próprios produtos.")
        produto.atualizar_quantidade(nova_quantidade)

    # --- pedidos ---
    def receber_pedido(self, pedido: Pedido) -> None:
        if pedido.empresa_marisqueira is not self:
            raise ErroRegraNegocio("Este pedido não pertence a esta empresa.")
        pedido.analise = SituacaoAnalise.AGUARDANDO_ANALISE
        self.pedidos_recebidos.append(pedido)

    def _validar_analise(self, pedido: Pedido) -> None:
        if pedido not in self.pedidos_recebidos:
            raise ErroRegraNegocio("Pedido não encontrado nesta empresa.")
        if pedido.analise != SituacaoAnalise.AGUARDANDO_ANALISE:
            raise ErroRegraNegocio(f"O pedido está '{pedido.analise.value}' e não pode ser analisado.")

    def aceitar_pedido(self, pedido: Pedido) -> None:
        self._validar_analise(pedido)
        if not pedido.verificar_disponibilidade():  # o estoque pode ter mudado (RN18)
            raise QuantidadeIndisponivelError("Estoque insuficiente para aceitar o pedido.")
        for item in pedido.itens:
            item.produto.atualizar_quantidade(item.produto.quantidade_disponivel - item.quantidade)
        pedido.analise = SituacaoAnalise.ACEITO
        pedido.status_pedido = StatusPedido.EM_PREPARO

    def rejeitar_pedido(self, pedido: Pedido) -> None:
        self._validar_analise(pedido)
        pedido.analise = SituacaoAnalise.REJEITADO

    def solicitar_ajuste(self, pedido: Pedido, motivo: str) -> None:
        self._validar_analise(pedido)
        if not motivo:
            raise ErroRegraNegocio("Informe o motivo do ajuste.")
        pedido.analise = SituacaoAnalise.AJUSTE_SOLICITADO
        pedido.motivo_ajuste = motivo

    def atualizar_status_entrega(self, pedido: Pedido, novo_status: StatusPedido) -> None:
        """RN22: a própria empresa entrega e atualiza o status (sem rastreamento em tempo real).
        Sequência: em preparo -> em curso -> finalizado."""
        if pedido not in self.pedidos_recebidos or pedido.analise != SituacaoAnalise.ACEITO:
            raise ErroRegraNegocio("Só é possível atualizar a entrega de pedidos aceitos.")
        if novo_status not in _ORDEM_STATUS:
            raise ErroRegraNegocio("Status de pedido inválido.")
        atual = _ORDEM_STATUS.index(pedido.status_pedido)
        if _ORDEM_STATUS.index(novo_status) != atual + 1:
            raise ErroRegraNegocio(
                f"Transição inválida: de '{pedido.status_pedido.value}' para '{novo_status.value}'.")
        pedido.status_pedido = novo_status

    # --- situação / reputação ---
    def situacao(self, agora: time | None = None) -> SituacaoEmpresa:
        """RN19/RN20: verde = disponível, laranja = estoque baixo, vermelho = fora do horário."""
        agora = agora or datetime.now().time()
        if not (self.abertura <= agora <= self.fechamento):
            return SituacaoEmpresa.FORA_DO_HORARIO
        if sum(p.quantidade_disponivel for p in self.produtos) < LIMITE_ESTOQUE_BAIXO_KG:
            return SituacaoEmpresa.ESTOQUE_BAIXO
        return SituacaoEmpresa.DISPONIVEL

    @property
    def media_avaliacoes(self) -> float:
        notas = [a.nota for a in self.avaliacoes if a.nota]
        return sum(notas) / len(notas) if notas else 0.0

    def __repr__(self) -> str:
        return f"EmpresaMarisqueira({self.nome!r})"
