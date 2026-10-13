"""Enumerações do domínio."""
from enum import Enum


class Categoria(Enum):
    """Categoria do produto: fresco ou congelado."""
    FRESCO = "fresco"
    CONGELADO = "congelado"


class StatusPedido(Enum):
    """status_pedido: em preparo, em curso (a caminho da entrega) e finalizado."""
    EM_PREPARO = "em preparo"
    EM_CURSO = "em curso"
    FINALIZADO = "finalizado"


class SituacaoAnalise(Enum):
    """Análise do pedido pela marisqueira (fluxo P7): aceite, rejeição ou ajuste."""
    RASCUNHO = "rascunho"
    AGUARDANDO_ANALISE = "aguardando análise"
    ACEITO = "aceito"
    REJEITADO = "rejeitado"
    AJUSTE_SOLICITADO = "ajuste solicitado"


class SituacaoEmpresa(Enum):
    """Indicador visual da empresa (RN20)."""
    DISPONIVEL = "verde"
    ESTOQUE_BAIXO = "laranja"
    FORA_DO_HORARIO = "vermelho"
