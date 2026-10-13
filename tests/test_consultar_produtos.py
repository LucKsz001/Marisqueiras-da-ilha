import pytest

from marisqueiras_da_ilha import Categoria, EmpresaCompradora, ErroRegraNegocio


def test_sem_filtros_retorna_todos(comprador, catalogo):
    assert len(comprador.consultar_produtos(catalogo)) == 3


def test_filtro_por_nome(comprador, catalogo):
    assert {p.nome for p in comprador.consultar_produtos(catalogo, nome="sur")} == {"Sururu"}


def test_filtro_por_categoria(comprador, catalogo):
    res = comprador.consultar_produtos(catalogo, categoria=Categoria.CONGELADO)
    assert len(res) == 1 and res[0].categoria == Categoria.CONGELADO


def test_filtro_por_empresa(comprador, catalogo):
    assert [p.nome for p in comprador.consultar_produtos(catalogo, empresa="Ana")] == ["Camarão"]


def test_filtro_por_localizacao(comprador, catalogo, ana):
    ana.localizacao = "Raposa"
    assert [p.nome for p in comprador.consultar_produtos(catalogo, localizacao="raposa")] == ["Camarão"]


def test_filtro_por_avaliacao(comprador, maria, catalogo, pedido_finalizado):
    comprador.avaliar_empresa(pedido_finalizado(comprador, maria, maria.produtos[0]), 5)
    res = comprador.consultar_produtos(catalogo, avaliacao_minima=4)
    assert res and all(p.empresa is maria for p in res)


def test_filtros_combinados(comprador, catalogo):
    res = comprador.consultar_produtos(catalogo, nome="sururu", categoria=Categoria.FRESCO)
    assert len(res) == 1


def test_produto_indisponivel_continua_aparecendo(comprador, maria, catalogo):
    maria.alterar_quantidade(maria.produtos[0], 0)
    assert maria.produtos[0] in comprador.consultar_produtos(catalogo)


def test_ordena_por_menor_e_maior_preco(comprador, catalogo):
    menor = comprador.consultar_produtos(catalogo, ordenar_por="menor_preco")
    maior = comprador.consultar_produtos(catalogo, ordenar_por="maior_preco")
    assert [p.preco for p in menor] == [28.0, 30.0, 45.0]
    assert [p.preco for p in maior] == [45.0, 30.0, 28.0]


def test_ordena_por_melhor_avaliacao(comprador, maria, ana, catalogo, pedido_finalizado):
    comprador.avaliar_empresa(pedido_finalizado(comprador, ana, ana.produtos[0], 25), 5)
    comprador.avaliar_empresa(pedido_finalizado(comprador, maria, maria.produtos[0]), 3)
    assert comprador.consultar_produtos(catalogo, ordenar_por="melhor_avaliacao")[0].empresa is ana


def test_ordena_por_proximidade(ana, catalogo):
    perto = EmpresaCompradora("11444777000161", "Perto", "Vila Maresia")
    ana.localizacao = "Outra Ilha"
    assert perto.consultar_produtos(catalogo, ordenar_por="proximidade")[-1].empresa is ana


def test_ordenacao_invalida(comprador, catalogo):
    with pytest.raises(ErroRegraNegocio):
        comprador.consultar_produtos(catalogo, ordenar_por="cor")
