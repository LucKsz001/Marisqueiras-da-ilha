import pytest

from marisqueiras_da_ilha import (
    Categoria, ErroRegraNegocio, QuantidadeIndisponivelError, SituacaoAnalise,
)


def test_pedido_chega_na_marisqueira(comprador, maria, sururu):
    pedido = comprador.realizar_pedido([(sururu, 50)], "Av. Litorânea, 100", "2 dias")
    assert pedido in maria.pedidos_recebidos and pedido in comprador.pedidos
    assert pedido.analise == SituacaoAnalise.AGUARDANDO_ANALISE
    assert pedido.endereco_entrega == "Av. Litorânea, 100" and pedido.tempo_entrega == "2 dias"


def test_pedido_com_varios_produtos_da_mesma_empresa(comprador, maria, sururu):
    congelado = maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)
    pedido = comprador.realizar_pedido([(sururu, 50), (congelado, 25)], "End", "1 dia")
    assert len(pedido.itens) == 2 and pedido.total == 50 * 30 + 25 * 28


def test_nao_ha_valor_minimo_em_dinheiro(comprador, maria):
    barato = maria.cadastrar_produto("Casquinha", Categoria.FRESCO, 0.5, 100)
    assert comprador.realizar_pedido([(barato, 25)], "End", "1 dia").total == 12.5


def test_sem_itens(comprador):
    with pytest.raises(ErroRegraNegocio):
        comprador.realizar_pedido([], "End", "1 dia")


def test_abaixo_do_minimo_por_produto(comprador, sururu):
    with pytest.raises(ErroRegraNegocio):
        comprador.realizar_pedido([(sururu, 10)], "End", "1 dia")


def test_acima_do_estoque(comprador, camarao):
    with pytest.raises(QuantidadeIndisponivelError):
        comprador.realizar_pedido([(camarao, 500)], "End", "1 dia")


def test_empresas_diferentes_no_mesmo_pedido(comprador, sururu, camarao):
    with pytest.raises(ErroRegraNegocio):
        comprador.realizar_pedido([(sururu, 25), (camarao, 25)], "End", "1 dia")


@pytest.mark.parametrize("endereco,tempo", [("", "1 dia"), ("End", "")])
def test_endereco_e_tempo_obrigatorios(comprador, sururu, endereco, tempo):
    with pytest.raises(ErroRegraNegocio):
        comprador.realizar_pedido([(sururu, 25)], endereco, tempo)


def test_pedido_invalido_nao_chega_na_marisqueira(comprador, maria, sururu):
    with pytest.raises(ErroRegraNegocio):
        comprador.realizar_pedido([(sururu, 5)], "End", "1 dia")
    assert maria.pedidos_recebidos == [] and comprador.pedidos == []
