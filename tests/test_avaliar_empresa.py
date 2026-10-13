import pytest

from marisqueiras_da_ilha import ErroRegraNegocio


def test_avalia_apos_pedido_finalizado(comprador, maria, sururu, pedido_finalizado):
    av = comprador.avaliar_empresa(pedido_finalizado(comprador, maria, sururu), 4)
    assert av.nota == 4 and av.empresa is maria
    assert maria.media_avaliacoes == 4.0


def test_media_de_varias_avaliacoes(comprador, maria, sururu, pedido_finalizado):
    comprador.avaliar_empresa(pedido_finalizado(comprador, maria, sururu, 25), 5)
    comprador.avaliar_empresa(pedido_finalizado(comprador, maria, sururu, 25), 4)
    assert maria.media_avaliacoes == 4.5


def test_nao_avalia_pedido_nao_finalizado(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    with pytest.raises(ErroRegraNegocio):
        comprador.avaliar_empresa(pedido, 5)


def test_nao_avalia_pedido_em_curso(comprador, maria, sururu):
    from marisqueiras_da_ilha import StatusPedido
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    maria.atualizar_status_entrega(pedido, StatusPedido.EM_CURSO)
    with pytest.raises(ErroRegraNegocio):
        comprador.avaliar_empresa(pedido, 5)


def test_nao_avalia_duas_vezes_o_mesmo_pedido(comprador, maria, sururu, pedido_finalizado):
    pedido = pedido_finalizado(comprador, maria, sururu)
    comprador.avaliar_empresa(pedido, 5)
    with pytest.raises(ErroRegraNegocio):
        comprador.avaliar_empresa(pedido, 5)
    assert len(maria.avaliacoes) == 1


def test_outro_comprador_nao_avalia_pedido_alheio(comprador, outro_comprador, maria, sururu, pedido_finalizado):
    pedido = pedido_finalizado(comprador, maria, sururu)
    with pytest.raises(ErroRegraNegocio):
        outro_comprador.avaliar_empresa(pedido, 5)


def test_nota_invalida_nao_marca_pedido_como_avaliado(comprador, maria, sururu, pedido_finalizado):
    pedido = pedido_finalizado(comprador, maria, sururu)
    with pytest.raises(ErroRegraNegocio):
        comprador.avaliar_empresa(pedido, 9)
    assert not pedido.avaliado
    comprador.avaliar_empresa(pedido, 5)
