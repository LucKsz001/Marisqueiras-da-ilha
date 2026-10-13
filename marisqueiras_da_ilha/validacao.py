"""Funções de validação reutilizadas pelas empresas."""
from __future__ import annotations

import re

from .excecoes import ErroRegraNegocio


def validar_cnpj(cnpj: str) -> str:
    """Valida o CNPJ (14 dígitos + dígitos verificadores) e devolve só os números."""
    digitos = re.sub(r"\D", "", str(cnpj or ""))
    if len(digitos) != 14 or digitos == digitos[0] * 14:
        raise ErroRegraNegocio("CNPJ inválido: deve ter 14 dígitos.")

    def dv(base: str) -> str:
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2][-len(base):]
        resto = sum(int(d) * p for d, p in zip(base, pesos)) % 11
        return "0" if resto < 2 else str(11 - resto)

    d1 = dv(digitos[:12])
    d2 = dv(digitos[:12] + d1)
    if digitos[12:] != d1 + d2:
        raise ErroRegraNegocio("CNPJ inválido: dígitos verificadores incorretos.")
    return digitos
