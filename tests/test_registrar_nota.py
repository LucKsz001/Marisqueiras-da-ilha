import pytest

from marisqueiras_da_ilha import Avaliacao, ErroRegraNegocio


@pytest.fixture
def avaliacao(comprador, maria, sururu, pedido_finalizado):
    return Avaliacao(comprador, maria, pedido_finalizado(comprador, maria, sururu))


def test_atributos_iniciais(avaliacao):
    assert isinstance(avaliacao.id_avaliacao, int)
    assert avaliacao.nota is None


@pytest.mark.parametrize("nota", [1, 2, 3, 4, 5])
def test_notas_validas(avaliacao, maria, nota):
    avaliacao.registrar_nota(nota)
    assert avaliacao.nota == nota and avaliacao in maria.avaliacoes


@pytest.mark.parametrize("nota", [0, 6, -1, 3.5, "5", None, True])
def test_notas_invalidas(avaliacao, maria, nota):
    with pytest.raises(ErroRegraNegocio):
        avaliacao.registrar_nota(nota)
    assert avaliacao.nota is None and maria.avaliacoes == []


def test_ids_sao_unicos(comprador, maria, sururu, pedido_finalizado):
    p = pedido_finalizado(comprador, maria, sururu)
    assert Avaliacao(comprador, maria, p).id_avaliacao != Avaliacao(comprador, maria, p).id_avaliacao
