import pytest

from marisqueiras_da_ilha import Categoria, ErroRegraNegocio


def test_cadastra_produto(maria):
    p = maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 100)
    assert p in maria.produtos and p.empresa is maria


def test_fotografia_opcional(maria):
    assert maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 100).fotografia is None
    p = maria.cadastrar_produto("Ostra", Categoria.FRESCO, 50.0, 100, fotografia="ostra.jpg")
    assert p.fotografia == "ostra.jpg"


def test_fresco_e_congelado_sao_produtos_diferentes(maria):
    fresco = maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 100)
    congelado = maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 100)
    assert fresco is not congelado and len(maria.produtos) == 2


def test_nao_cadastra_duplicado_na_mesma_categoria(maria):
    maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 100)
    with pytest.raises(ErroRegraNegocio):
        maria.cadastrar_produto("sururu", Categoria.FRESCO, 31.0, 100)
    assert len(maria.produtos) == 1


@pytest.mark.parametrize("nome,cat,preco,qtd", [
    ("", Categoria.FRESCO, 30.0, 100),
    ("Sururu", None, 30.0, 100),
    ("Sururu", Categoria.FRESCO, None, 100),
    ("Sururu", Categoria.FRESCO, 30.0, None),
    ("Sururu", Categoria.FRESCO, 30.0, 24),
])
def test_dados_obrigatorios(maria, nome, cat, preco, qtd):
    with pytest.raises(ErroRegraNegocio):
        maria.cadastrar_produto(nome, cat, preco, qtd)
    assert maria.produtos == []
