import pytest

from marisqueiras_da_ilha import EmpresaCompradora, ErroRegraNegocio


def test_atributos_da_compradora():
    c = EmpresaCompradora("11.444.777/0001-61", "Restaurante Mar Azul", "São Luís")
    assert c.id_empresa_compradora == "11444777000161"
    assert c.nome == "Restaurante Mar Azul"
    assert c.localizacao == "São Luís"
    assert c.pedidos == []


@pytest.mark.parametrize("cnpj", ["", "123", "11444777000162"])
def test_cnpj_invalido(cnpj):
    with pytest.raises(ErroRegraNegocio):
        EmpresaCompradora(cnpj, "Restaurante", "São Luís")


@pytest.mark.parametrize("nome,localizacao", [("", "São Luís"), ("Restaurante", ""), (None, None)])
def test_nome_e_localizacao_obrigatorios(nome, localizacao):
    with pytest.raises(ErroRegraNegocio):
        EmpresaCompradora("11444777000161", nome, localizacao)
