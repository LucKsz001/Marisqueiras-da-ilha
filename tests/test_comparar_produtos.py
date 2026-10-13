import pytest

from marisqueiras_da_ilha import ErroRegraNegocio


def test_compara_produtos_de_empresas_diferentes_ordenando_por_preco(comprador, sururu, camarao):
    tabela = comprador.comparar_produtos([camarao, sururu])
    assert [t["empresa"] for t in tabela] == ["Marisqueira da Maria", "Marisqueira da Ana"]
    assert tabela[0]["preco"] == 30.0 and tabela[1]["preco"] == 45.0


def test_resultado_traz_os_dados_para_comparacao(comprador, sururu, camarao):
    linha = comprador.comparar_produtos([sururu, camarao])[0]
    assert set(linha) == {"produto", "categoria", "empresa", "preco", "disponivel_kg", "avaliacao", "localizacao"}


def test_exige_ao_menos_dois_produtos(comprador, sururu):
    with pytest.raises(ErroRegraNegocio):
        comprador.comparar_produtos([sururu])
    with pytest.raises(ErroRegraNegocio):
        comprador.comparar_produtos([])
