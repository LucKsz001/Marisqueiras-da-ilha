import pytest

from marisqueiras_da_ilha import ErroRegraNegocio, validar_cnpj


def test_cnpj_valido_com_ou_sem_formatacao():
    assert validar_cnpj("11222333000181") == "11222333000181"
    assert validar_cnpj("11.222.333/0001-81") == "11222333000181"


@pytest.mark.parametrize("cnpj", ["", None, "123", "11222333000182", "00000000000000", "abc", "112223330001811"])
def test_cnpj_invalido(cnpj):
    with pytest.raises(ErroRegraNegocio):
        validar_cnpj(cnpj)
