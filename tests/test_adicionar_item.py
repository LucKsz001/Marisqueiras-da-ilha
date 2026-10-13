import pytest

from marisqueiras_da_ilha import (
    Categoria, ErroRegraNegocio, Pedido, QuantidadeIndisponivelError, SituacaoAnalise,
)


@pytest.fixture
def pedido(comprador):
    return Pedido(comprador, "End", "1 dia")


def test_adiciona_item_e_define_a_empresa_do_pedido(pedido, sururu):
    item = pedido.adicionar_item(sururu, 25)
    assert item in pedido.itens
    assert pedido.empresa_marisqueira is sururu.empresa


def test_varios_produtos_da_mesma_empresa(pedido, maria, sururu):
    congelado = maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)
    pedido.adicionar_item(sururu, 50)
    pedido.adicionar_item(congelado, 25)
    assert len(pedido.itens) == 2


def test_nao_mistura_empresas(pedido, sururu, camarao):
    pedido.adicionar_item(sururu, 25)
    with pytest.raises(ErroRegraNegocio):
        pedido.adicionar_item(camarao, 25)


def test_rejeita_abaixo_do_minimo(pedido, sururu):
    with pytest.raises(ErroRegraNegocio):
        pedido.adicionar_item(sururu, 10)
    assert pedido.itens == []


def test_rejeita_acima_do_estoque(pedido, camarao):
    with pytest.raises(QuantidadeIndisponivelError):
        pedido.adicionar_item(camarao, 81)
    assert pedido.itens == []


def test_aceita_quantidade_igual_ao_estoque(pedido, camarao):
    pedido.adicionar_item(camarao, 80)


def test_rejeita_produto_repetido(pedido, sururu):
    pedido.adicionar_item(sururu, 25)
    with pytest.raises(ErroRegraNegocio):
        pedido.adicionar_item(sururu, 25)


def test_nao_adiciona_apos_o_pedido_ser_enviado(pedido, sururu):
    pedido.analise = SituacaoAnalise.AGUARDANDO_ANALISE
    with pytest.raises(ErroRegraNegocio):
        pedido.adicionar_item(sururu, 25)
