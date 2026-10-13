"""Fixtures compartilhadas pelos testes (fica na raiz para a pasta tests/ conter só testes)."""
import pytest

from marisqueiras_da_ilha import (
    Categoria, EmpresaCompradora, EmpresaMarisqueira, StatusPedido,
)

# CNPJs válidos (com dígitos verificadores corretos)
CNPJ_MARIA = "11222333000181"
CNPJ_ANA = "45997418000153"
CNPJ_COMPRADOR = "11444777000161"
CNPJ_OUTRO = "12345678000195"


@pytest.fixture
def maria():
    return EmpresaMarisqueira(CNPJ_MARIA, "Marisqueira da Maria", "Vila Maresia")


@pytest.fixture
def ana():
    return EmpresaMarisqueira(CNPJ_ANA, "Marisqueira da Ana", "Vila Maresia")


@pytest.fixture
def comprador():
    return EmpresaCompradora(CNPJ_COMPRADOR, "Restaurante Mar Azul", "São Luís")


@pytest.fixture
def outro_comprador():
    return EmpresaCompradora(CNPJ_OUTRO, "Outro Restaurante", "São Luís")


@pytest.fixture
def sururu(maria):
    return maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 200)


@pytest.fixture
def camarao(ana):
    return ana.cadastrar_produto("Camarão", Categoria.FRESCO, 45.0, 80)


@pytest.fixture
def catalogo(maria, ana):
    maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 200)
    maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)
    ana.cadastrar_produto("Camarão", Categoria.FRESCO, 45.0, 80)
    return [maria, ana]


@pytest.fixture
def pedido_finalizado():
    """Fábrica: cria um pedido aceito e levado até 'finalizado'."""
    def _fazer(comprador, marisqueira, produto, quantidade=50):
        pedido = comprador.realizar_pedido([(produto, quantidade)], "Av. Litorânea, 100", "2 dias")
        marisqueira.aceitar_pedido(pedido)
        marisqueira.atualizar_status_entrega(pedido, StatusPedido.EM_CURSO)
        marisqueira.atualizar_status_entrega(pedido, StatusPedido.FINALIZADO)
        return pedido
    return _fazer
