import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, StatusPedido


@pytest.fixture
def pedido_aceito(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    maria.aceitar_pedido(pedido)
    return pedido


def test_sequencia_em_preparo_em_curso_finalizado(maria, pedido_aceito):
    assert pedido_aceito.status_pedido == StatusPedido.EM_PREPARO
    maria.atualizar_status_entrega(pedido_aceito, StatusPedido.EM_CURSO)
    assert pedido_aceito.status_pedido == StatusPedido.EM_CURSO
    maria.atualizar_status_entrega(pedido_aceito, StatusPedido.FINALIZADO)
    assert pedido_aceito.status_pedido == StatusPedido.FINALIZADO


def test_nao_pula_etapas(maria, pedido_aceito):
    with pytest.raises(ErroRegraNegocio):
        maria.atualizar_status_entrega(pedido_aceito, StatusPedido.FINALIZADO)


def test_nao_volta_etapas(maria, pedido_aceito):
    maria.atualizar_status_entrega(pedido_aceito, StatusPedido.EM_CURSO)
    with pytest.raises(ErroRegraNegocio):
        maria.atualizar_status_entrega(pedido_aceito, StatusPedido.EM_PREPARO)


def test_status_invalido(maria, pedido_aceito):
    with pytest.raises(ErroRegraNegocio):
        maria.atualizar_status_entrega(pedido_aceito, "entregue")


def test_so_para_pedido_aceito(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "End", "1 dia")
    with pytest.raises(ErroRegraNegocio):
        maria.atualizar_status_entrega(pedido, StatusPedido.EM_CURSO)


def test_so_a_marisqueira_do_pedido_atualiza(ana, pedido_aceito):
    with pytest.raises(ErroRegraNegocio):
        ana.atualizar_status_entrega(pedido_aceito, StatusPedido.EM_CURSO)
