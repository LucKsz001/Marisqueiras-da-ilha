from marisqueiras_da_ilha import ItemPedido, Pedido


def test_atributos_do_item(comprador, sururu):
    pedido = Pedido(comprador, "End", "1 dia")
    item = ItemPedido(pedido, sururu, 50)
    assert item.id_pedido == pedido.id_pedido
    assert item.id_produto == sururu.id_produto
    assert item.quantidade == 50


def test_preco_fica_fixado_no_item(comprador, sururu):
    item = ItemPedido(Pedido(comprador, "End", "1 dia"), sururu, 50)
    sururu.preco = 99.0
    assert item.preco_unitario == 30.0


def test_subtotal(comprador, sururu):
    assert ItemPedido(Pedido(comprador, "End", "1 dia"), sururu, 50).subtotal == 1500.0
