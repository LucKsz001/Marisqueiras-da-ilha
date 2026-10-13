import pytest

from marisqueiras_da_ilha import ErroRegraNegocio


def test_atualiza_quantidade(sururu):
    sururu.atualizar_quantidade(300)
    assert sururu.quantidade_disponivel == 300


def test_zero_e_permitido_e_produto_continua_cadastrado(maria, sururu):
    sururu.atualizar_quantidade(0)
    assert sururu.quantidade_disponivel == 0
    assert sururu in maria.produtos


def test_negativa_e_rejeitada(sururu):
    with pytest.raises(ErroRegraNegocio):
        sururu.atualizar_quantidade(-1)
    assert sururu.quantidade_disponivel == 200
