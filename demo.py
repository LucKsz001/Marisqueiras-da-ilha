"""Demonstração do projeto. Execute: python demo.py"""
from datetime import time

from marisqueiras_da_ilha import (
    Categoria, EmpresaCompradora, EmpresaMarisqueira, ErroRegraNegocio, StatusPedido,
)


def main() -> None:
    maria = EmpresaMarisqueira("11222333000181", "Marisqueira da Maria", "Vila Maresia")
    ana = EmpresaMarisqueira("45997418000153", "Marisqueira da Ana", "Vila Maresia")
    restaurante = EmpresaCompradora("11444777000161", "Restaurante Mar Azul", "São Luís")

    sururu_f = maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 200)
    sururu_c = maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)  # produto diferente
    camarao = ana.cadastrar_produto("Camarão", Categoria.FRESCO, 45.0, 80)

    print("Busca (sururu, menor preço):",
          restaurante.consultar_produtos([maria, ana], nome="sururu", ordenar_por="menor_preco"))
    print("Comparação:", restaurante.comparar_produtos([sururu_f, camarao]))

    pedido = restaurante.realizar_pedido([(sururu_f, 50), (sururu_c, 25)], "Av. Litorânea, 100", "2 dias")
    print(f"Pedido {pedido.id_pedido}: {pedido.analise.value} - total R${pedido.total:.2f}")

    maria.aceitar_pedido(pedido)
    print("status_pedido:", pedido.status_pedido.value)
    maria.atualizar_status_entrega(pedido, StatusPedido.EM_CURSO)
    maria.atualizar_status_entrega(pedido, StatusPedido.FINALIZADO)
    restaurante.avaliar_empresa(pedido, 5)
    print("Média da Maria:", maria.media_avaliacoes, "| Estoque sururu fresco:", sururu_f.quantidade_disponivel)
    print("Situação da Maria às 10h:", maria.situacao(time(10, 0)).value)

    # Regras sendo bloqueadas
    for descricao, tentativa in [
        ("abaixo de 25 kg", lambda: restaurante.realizar_pedido([(sururu_f, 10)], "End", "1 dia")),
        ("acima do estoque", lambda: restaurante.realizar_pedido([(camarao, 500)], "End", "1 dia")),
        ("empresas diferentes", lambda: restaurante.realizar_pedido([(sururu_f, 25), (camarao, 25)], "End", "1 dia")),
    ]:
        try:
            tentativa()
        except ErroRegraNegocio as e:
            print(f"Bloqueado ({descricao}): {e}")


if __name__ == "__main__":
    main()
