import pytest

from marisqueiras_da_ilha import (
    ErroRegraNegocio, QuantidadeIndisponivelError, SituacaoAnalise, StatusPedido,
)


def test_aceita_e_pedido_fica_em_preparo(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    assert pedido.analise == SituacaoAnalise.ACEITO
    assert pedido.status_pedido == StatusPedido.EM_PREPARO


def test_desconta_o_estoque(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    assert sururu.quantidade_disponivel == 150


def test_esgotar_o_estoque_deixa_produto_indisponivel_mas_cadastrado(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 200)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    assert sururu.indisponivel and sururu in maria.produtos


def test_falha_se_o_estoque_mudou_e_nao_desconta_nada(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 100)], "End", "1 dia")
    maria.alterar_quantidade(sururu, 50)
    with pytest.raises(QuantidadeIndisponivelError):
        maria.aceitar_pedido(pedido)
    assert sururu.quantidade_disponivel == 50
    assert pedido.status_pedido is None


def test_nao_aceita_pedido_ja_analisado(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    with pytest.raises(ErroRegraNegocio):
        maria.aceitar_pedido(pedido)


def test_outra_marisqueira_nao_aceita(comprador, ana, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    with pytest.raises(ErroRegraNegocio):
        ana.aceitar_pedido(pedido)
