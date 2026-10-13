import pytest

from marisqueiras_da_ilha import Categoria, ErroRegraNegocio, Pedido, SituacaoAnalise


def test_atributos_do_pedido(comprador):
    p = Pedido(comprador, "Av. Litorânea, 100", "2 dias")
    assert isinstance(p.id_pedido, int)
    assert p.endereco_entrega == "Av. Litorânea, 100"
    assert p.tempo_entrega == "2 dias"
    assert p.comprador is comprador
    assert p.itens == []


def test_status_pedido_so_existe_apos_aceite(comprador):
    p = Pedido(comprador, "End", "1 dia")
    assert p.status_pedido is None
    assert p.analise == SituacaoAnalise.RASCUNHO


def test_ids_sao_unicos(comprador):
    assert Pedido(comprador, "End", "1 dia").id_pedido != Pedido(comprador, "End", "1 dia").id_pedido


@pytest.mark.parametrize("endereco,tempo", [("", "1 dia"), ("End", ""), (None, None)])
def test_endereco_e_tempo_obrigatorios(comprador, endereco, tempo):
    with pytest.raises(ErroRegraNegocio):
        Pedido(comprador, endereco, tempo)


def test_total_soma_os_itens(comprador, maria, sururu):
    congelado = maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)
    p = Pedido(comprador, "End", "1 dia")
    p.adicionar_item(sururu, 50)
    p.adicionar_item(congelado, 25)
    assert p.total == 50 * 30 + 25 * 28


def test_verificar_disponibilidade_do_pedido(comprador, maria, sururu):
    p = Pedido(comprador, "End", "1 dia")
    p.adicionar_item(sururu, 100)
    assert p.verificar_disponibilidade()
    maria.alterar_quantidade(sururu, 50)
    assert not p.verificar_disponibilidade()
