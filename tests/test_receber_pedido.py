import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, Pedido, SituacaoAnalise


def _pedido(comprador, produto):
    p = Pedido(comprador, "End", "1 dia")
    p.adicionar_item(produto, 25)
    return p


def test_recebe_pedido_e_fica_aguardando_analise(comprador, maria, sururu):
    pedido = _pedido(comprador, sururu)
    maria.receber_pedido(pedido)
    assert pedido in maria.pedidos_recebidos
    assert pedido.analise == SituacaoAnalise.AGUARDANDO_ANALISE


def test_nao_recebe_pedido_de_outra_empresa(comprador, ana, sururu):
    with pytest.raises(ErroRegraNegocio):
        ana.receber_pedido(_pedido(comprador, sururu))
    assert ana.pedidos_recebidos == []
