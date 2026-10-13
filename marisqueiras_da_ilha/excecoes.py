"""Exceções de regra de negócio."""


class ErroRegraNegocio(ValueError):
    """Violação de uma regra de negócio do projeto."""


class QuantidadeIndisponivelError(ErroRegraNegocio):
    """RN18: quantidade solicitada maior que a disponível."""
