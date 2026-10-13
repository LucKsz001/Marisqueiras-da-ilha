import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, SituacaoAnalise


def test_rejeita_sem_mexer_no_estoque(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.rejeitar_pedido(pedido)
    assert pedido.analise == SituacaoAnalise.REJEITADO
    assert pedido.status_pedido is None
    assert sururu.quantidade_disponivel == 200


def test_nao_rejeita_pedido_ja_aceito(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    with pytest.raises(ErroRegraNegocio):
        maria.rejeitar_pedido(pedido)


def test_outra_marisqueira_nao_rejeita(comprador, ana, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    with pytest.raises(ErroRegraNegocio):
        ana.rejeitar_pedido(pedido)
