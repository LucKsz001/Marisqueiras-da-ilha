import pytest

from marisqueiras_da_ilha import ErroRegraNegocio


def test_altera_quantidade_do_proprio_produto(maria, sururu):
    maria.alterar_quantidade(sururu, 300)
    assert sururu.quantidade_disponivel == 300


def test_pode_zerar_e_produto_continua_cadastrado(maria, sururu):
    maria.alterar_quantidade(sururu, 0)
    assert sururu in maria.produtos and sururu.indisponivel


def test_nao_altera_produto_de_outra_empresa(ana, sururu):
    with pytest.raises(ErroRegraNegocio):
        ana.alterar_quantidade(sururu, 50)
    assert sururu.quantidade_disponivel == 200


def test_quantidade_negativa_rejeitada(maria, sururu):
    with pytest.raises(ErroRegraNegocio):
        maria.alterar_quantidade(sururu, -5)
