import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, ItemPedido, Pedido


def _item(comprador, produto, qtd):
    return ItemPedido(Pedido(comprador, "End", "1 dia"), produto, qtd)


def test_exatamente_25kg_e_valido(comprador, sururu):
    _item(comprador, sururu, 25).validar_quantidade()


def test_acima_de_25kg_e_valido(comprador, sururu):
    _item(comprador, sururu, 100).validar_quantidade()


@pytest.mark.parametrize("qtd", [0, 10, 24.9])
def test_abaixo_de_25kg_e_rejeitado(comprador, sururu, qtd):
    with pytest.raises(ErroRegraNegocio):
        _item(comprador, sururu, qtd).validar_quantidade()
