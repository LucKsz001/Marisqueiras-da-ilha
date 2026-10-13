import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, SituacaoAnalise


def test_solicita_ajuste_com_motivo(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.solicitar_ajuste(pedido, "Reduzir quantidade")
    assert pedido.analise == SituacaoAnalise.AJUSTE_SOLICITADO
    assert pedido.motivo_ajuste == "Reduzir quantidade"
    assert sururu.quantidade_disponivel == 200


@pytest.mark.parametrize("motivo", ["", None])
def test_motivo_e_obrigatorio(comprador, maria, sururu, motivo):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    with pytest.raises(ErroRegraNegocio):
        maria.solicitar_ajuste(pedido, motivo)
    assert pedido.analise == SituacaoAnalise.AGUARDANDO_ANALISE


def test_nao_pede_ajuste_de_pedido_ja_rejeitado(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.rejeitar_pedido(pedido)
    with pytest.raises(ErroRegraNegocio):
        maria.solicitar_ajuste(pedido, "Tarde demais")
