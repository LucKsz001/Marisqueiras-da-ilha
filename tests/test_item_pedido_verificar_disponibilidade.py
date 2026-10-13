from marisqueiras_da_ilha import ItemPedido, Pedido


def _item(comprador, produto, qtd):
    return ItemPedido(Pedido(comprador, "End", "1 dia"), produto, qtd)


def test_disponivel_ate_o_limite_do_estoque(comprador, sururu):
    assert _item(comprador, sururu, 200).verificar_disponibilidade()


def test_indisponivel_acima_do_estoque(comprador, sururu):
    assert not _item(comprador, sururu, 201).verificar_disponibilidade()
