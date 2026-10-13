import pytest

from marisqueiras_da_ilha import Categoria, ErroRegraNegocio, Produto


def test_atributos_do_produto(maria):
    p = Produto(maria, "Sururu", Categoria.FRESCO, 30.0, 100)
    assert isinstance(p.id_produto, int)
    assert (p.nome, p.categoria, p.preco, p.quantidade_disponivel) == ("Sururu", Categoria.FRESCO, 30.0, 100)
    assert p.empresa is maria


def test_fotografia_e_opcional(maria):
    assert Produto(maria, "Sururu", Categoria.FRESCO, 30.0, 100).fotografia is None
    assert Produto(maria, "Sururu", Categoria.FRESCO, 30.0, 100, "foto.jpg").fotografia == "foto.jpg"


def test_ids_sao_unicos(maria):
    a = Produto(maria, "Sururu", Categoria.FRESCO, 30.0, 100)
    b = Produto(maria, "Sururu", Categoria.CONGELADO, 28.0, 100)
    assert a.id_produto != b.id_produto


@pytest.mark.parametrize("nome,cat,preco,qtd", [
    ("", Categoria.FRESCO, 30.0, 100),
    ("Sururu", None, 30.0, 100),
    ("Sururu", "fresco", 30.0, 100),  # precisa ser Categoria
    ("Sururu", Categoria.FRESCO, None, 100),
    ("Sururu", Categoria.FRESCO, 0, 100),
    ("Sururu", Categoria.FRESCO, 30.0, None),
    ("Sururu", Categoria.FRESCO, 30.0, 24),  # abaixo de 25 kg
])
def test_dados_invalidos(maria, nome, cat, preco, qtd):
    with pytest.raises(ErroRegraNegocio):
        Produto(maria, nome, cat, preco, qtd)


def test_produto_com_estoque_zero_fica_indisponivel(sururu):
    sururu.atualizar_quantidade(0)
    assert sururu.indisponivel
