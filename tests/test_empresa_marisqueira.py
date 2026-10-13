from datetime import time

import pytest

from marisqueiras_da_ilha import EmpresaMarisqueira, ErroRegraNegocio


def test_atributos_da_marisqueira():
    m = EmpresaMarisqueira("11.222.333/0001-81", "Marisqueira da Maria", "Vila Maresia")
    assert m.id_empresa_marisqueira == "11222333000181"
    assert m.nome == "Marisqueira da Maria"
    assert m.localizacao == "Vila Maresia"
    assert m.produtos == [] and m.pedidos_recebidos == [] and m.avaliacoes == []


def test_horario_padrao_e_personalizado():
    assert EmpresaMarisqueira("11222333000181", "M", "Vila").abertura == time(6, 0)
    m = EmpresaMarisqueira("11222333000181", "M", "Vila", abertura=time(8, 0), fechamento=time(12, 0))
    assert (m.abertura, m.fechamento) == (time(8, 0), time(12, 0))


@pytest.mark.parametrize("cnpj", ["", "123", "11222333000182"])
def test_cnpj_invalido(cnpj):
    with pytest.raises(ErroRegraNegocio):
        EmpresaMarisqueira(cnpj, "Maria", "Vila")


@pytest.mark.parametrize("nome,localizacao", [("", "Vila"), ("Maria", ""), (None, None)])
def test_nome_e_localizacao_obrigatorios(nome, localizacao):
    with pytest.raises(ErroRegraNegocio):
        EmpresaMarisqueira("11222333000181", nome, localizacao)


def test_media_sem_avaliacoes_e_zero(maria):
    assert maria.media_avaliacoes == 0.0
