"""Interface de terminal (menus) do projeto Marisqueiras da Ilha."""
from __future__ import annotations

from .empresa_compradora import EmpresaCompradora
from .empresa_marisqueira import EmpresaMarisqueira
from .enums import Categoria, SituacaoAnalise, StatusPedido
from .excecoes import ErroRegraNegocio
from .pedido import Pedido
from .produto import Produto

LINHA = "=" * 60


# ----------------------------------------------------------------------------
# Leitura de dados
# ----------------------------------------------------------------------------
def ler_texto(prompt: str, obrigatorio: bool = True) -> str:
    while True:
        valor = input(prompt).strip()
        if valor or not obrigatorio:
            return valor
        print("  Campo obrigatório.")


def ler_numero(prompt: str, minimo: float | None = None, opcional: bool = False) -> float | None:
    while True:
        valor = input(prompt).strip().replace(",", ".")
        if opcional and not valor:
            return None
        try:
            numero = float(valor)
        except ValueError:
            print("  Digite um número válido.")
            continue
        if minimo is not None and numero < minimo:
            print(f"  O valor deve ser no mínimo {minimo:g}.")
            continue
        return numero


def ler_inteiro(prompt: str, minimo: int, maximo: int) -> int:
    while True:
        valor = input(prompt).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"  Digite um número de {minimo} a {maximo}.")


def menu(titulo: str, opcoes: list[str], rotulo_zero: str = "Voltar") -> int:
    print(f"\n{LINHA}\n {titulo}\n{LINHA}")
    for i, texto in enumerate(opcoes, 1):
        print(f"  {i} - {texto}")
    print(f"  0 - {rotulo_zero}")
    return ler_inteiro("Escolha uma opção: ", 0, len(opcoes))


def escolher(itens: list, formatar, titulo: str):
    """Lista numerada; devolve o item escolhido ou None."""
    if not itens:
        print("  Nada para mostrar.")
        return None
    print(f"\n{titulo}")
    for i, item in enumerate(itens, 1):
        print(f"  {i}) {formatar(item)}")
    print("  0) Cancelar")
    n = ler_inteiro("Escolha: ", 0, len(itens))
    return itens[n - 1] if n else None


def escolher_categoria(opcional: bool = True) -> Categoria | None:
    print("  Categoria: 1 - fresco | 2 - congelado" + (" | Enter - todas" if opcional else ""))
    while True:
        v = input("  > ").strip()
        if v == "" and opcional:
            return None
        if v in ("1", "2"):
            return Categoria.FRESCO if v == "1" else Categoria.CONGELADO
        print("  Opção inválida.")


# ----------------------------------------------------------------------------
# Formatação
# ----------------------------------------------------------------------------
def kg(valor: float) -> str:
    return f"{valor:g} kg"


def fmt_produto(p: Produto, detalhado: bool = False) -> str:
    texto = f"[{p.id_produto}] {p.nome} ({p.categoria.value}) - R$ {p.preco:.2f}/kg - {kg(p.quantidade_disponivel)}"
    if p.indisponivel:
        texto += " - INDISPONÍVEL"
    if detalhado:
        media = p.empresa.media_avaliacoes
        nota = f"{media:.1f}★" if media else "sem avaliações"
        texto += f"\n      {p.empresa.nome} ({p.empresa.localizacao}) - {nota}"
    return texto


def fmt_pedido(p: Pedido) -> str:
    entrega = p.status_pedido.value if p.status_pedido else "-"
    linhas = [f"Pedido #{p.id_pedido} | {p.comprador.nome} -> {p.empresa_marisqueira.nome}",
              f"      análise: {p.analise.value} | entrega: {entrega} | total: R$ {p.total:.2f}",
              f"      entregar em: {p.endereco_entrega} ({p.tempo_entrega})"]
    for item in p.itens:
        linhas.append(f"        - {item.produto.nome} ({item.produto.categoria.value}): {kg(item.quantidade)}")
    if p.motivo_ajuste:
        linhas.append(f"      ajuste solicitado: {p.motivo_ajuste}")
    return "\n".join(linhas)


# ----------------------------------------------------------------------------
# Sistema
# ----------------------------------------------------------------------------
class Sistema:
    def __init__(self) -> None:
        self.marisqueiras: list[EmpresaMarisqueira] = []
        self.compradoras: list[EmpresaCompradora] = []
        self._dados_iniciais()

    def _dados_iniciais(self) -> None:
        maria = EmpresaMarisqueira("11222333000181", "Marisqueira da Maria", "Vila Maresia")
        ana = EmpresaMarisqueira("45997418000153", "Marisqueira da Ana", "Vila Maresia")
        maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 200)
        maria.cadastrar_produto("Sururu", Categoria.CONGELADO, 28.0, 150)
        maria.cadastrar_produto("Ostra", Categoria.FRESCO, 55.0, 60)
        ana.cadastrar_produto("Camarão", Categoria.FRESCO, 45.0, 80)
        ana.cadastrar_produto("Caranguejo", Categoria.CONGELADO, 38.0, 120)
        self.marisqueiras += [maria, ana]
        self.compradoras.append(EmpresaCompradora("11444777000161", "Restaurante Mar Azul", "São Luís"))

    @property
    def todos_produtos(self) -> list[Produto]:
        return [p for m in self.marisqueiras for p in m.produtos]

    # --- menu principal ---
    def executar(self) -> None:
        print(f"\n{LINHA}\n  MARISQUEIRAS DA ILHA\n{LINHA}")
        try:
            while True:
                op = menu("MENU PRINCIPAL", [
                    "Entrar como Empresa Marisqueira",
                    "Entrar como Empresa Compradora",
                    "Cadastrar nova empresa",
                ], "Sair")
                if op == 0:
                    break
                self._seguro(lambda: {1: self.entrar_marisqueira, 2: self.entrar_compradora,
                                      3: self.cadastrar_empresa}[op]())
        except (EOFError, KeyboardInterrupt):
            print()
        print("Até logo!")

    @staticmethod
    def _seguro(acao) -> None:
        try:
            acao()
        except ErroRegraNegocio as erro:
            print(f"\n  ✖ {erro}")

    def cadastrar_empresa(self) -> None:
        tipo = menu("CADASTRAR EMPRESA", ["Empresa Marisqueira", "Empresa Compradora"], "Cancelar")
        if tipo == 0:
            return
        cnpj = ler_texto("CNPJ: ")
        nome = ler_texto("Nome da empresa: ")
        localizacao = ler_texto("Localização: ")
        classe = EmpresaMarisqueira if tipo == 1 else EmpresaCompradora
        empresa = classe(cnpj, nome, localizacao)
        (self.marisqueiras if tipo == 1 else self.compradoras).append(empresa)
        print(f"\n  ✔ {empresa.nome} cadastrada.")

    # --- Marisqueira ---
    def entrar_marisqueira(self) -> None:
        m = escolher(self.marisqueiras, lambda e: f"{e.nome} ({e.localizacao})", "Qual empresa marisqueira?")
        if not m:
            return
        acoes = {
            1: lambda: self.m_cadastrar_produto(m), 2: lambda: self.m_listar_produtos(m),
            3: lambda: self.m_alterar_quantidade(m), 4: lambda: self.m_listar_pedidos(m),
            5: lambda: self.m_analisar(m, "aceitar"), 6: lambda: self.m_analisar(m, "rejeitar"),
            7: lambda: self.m_analisar(m, "ajuste"), 8: lambda: self.m_status_entrega(m),
            9: lambda: self.m_situacao(m),
        }
        while True:
            op = menu(f"MARISQUEIRA: {m.nome}", [
                "Cadastrar produto", "Listar meus produtos", "Alterar quantidade disponível",
                "Ver pedidos recebidos", "Aceitar pedido", "Rejeitar pedido",
                "Solicitar ajuste em pedido", "Atualizar status da entrega",
                "Situação da empresa e avaliações",
            ])
            if op == 0:
                return
            self._seguro(acoes[op])

    def m_cadastrar_produto(self, m: EmpresaMarisqueira) -> None:
        nome = ler_texto("Nome do produto: ")
        categoria = escolher_categoria(opcional=False)
        preco = ler_numero("Preço por kg (R$): ", minimo=0.01)
        qtd = ler_numero("Quantidade disponível (kg, mínimo 25): ", minimo=0)
        foto = ler_texto("Fotografia (arquivo/URL, Enter para pular): ", obrigatorio=False) or None
        p = m.cadastrar_produto(nome, categoria, preco, qtd, foto)
        print(f"\n  ✔ Produto cadastrado: {fmt_produto(p)}")

    def m_listar_produtos(self, m: EmpresaMarisqueira) -> None:
        print("\nMeus produtos:")
        if not m.produtos:
            print("  Nenhum produto cadastrado.")
        for p in m.produtos:
            print("  " + fmt_produto(p))

    def m_alterar_quantidade(self, m: EmpresaMarisqueira) -> None:
        p = escolher(m.produtos, fmt_produto, "Qual produto?")
        if p:
            nova = ler_numero("Nova quantidade disponível (kg): ", minimo=0)
            m.alterar_quantidade(p, nova)
            print(f"\n  ✔ {fmt_produto(p)}")

    def m_listar_pedidos(self, m: EmpresaMarisqueira) -> None:
        print("\nPedidos recebidos:")
        if not m.pedidos_recebidos:
            print("  Nenhum pedido recebido.")
        for p in m.pedidos_recebidos:
            print("  " + fmt_pedido(p))

    def m_analisar(self, m: EmpresaMarisqueira, acao: str) -> None:
        pendentes = [p for p in m.pedidos_recebidos if p.analise == SituacaoAnalise.AGUARDANDO_ANALISE]
        p = escolher(pendentes, fmt_pedido, "Pedidos aguardando análise:")
        if not p:
            return
        if acao == "aceitar":
            m.aceitar_pedido(p)
            print("\n  ✔ Pedido aceito. Estoque atualizado; status: em preparo.")
        elif acao == "rejeitar":
            m.rejeitar_pedido(p)
            print("\n  ✔ Pedido rejeitado.")
        else:
            m.solicitar_ajuste(p, ler_texto("Motivo do ajuste: "))
            print("\n  ✔ Ajuste solicitado.")

    def m_status_entrega(self, m: EmpresaMarisqueira) -> None:
        em_andamento = [p for p in m.pedidos_recebidos
                        if p.analise == SituacaoAnalise.ACEITO and p.status_pedido != StatusPedido.FINALIZADO]
        p = escolher(em_andamento, fmt_pedido, "Pedidos em andamento:")
        if not p:
            return
        novo = menu("NOVO STATUS", ["Em curso (a caminho da entrega)", "Finalizado"], "Cancelar")
        if novo:
            m.atualizar_status_entrega(p, StatusPedido.EM_CURSO if novo == 1 else StatusPedido.FINALIZADO)
            print(f"\n  ✔ Status atualizado: {p.status_pedido.value}.")

    def m_situacao(self, m: EmpresaMarisqueira) -> None:
        media = m.media_avaliacoes
        print(f"\n  Situação: {m.situacao().value}  (verde = disponível, laranja = estoque baixo, "
              f"vermelho = fora do horário {m.abertura:%H:%M}-{m.fechamento:%H:%M})")
        print(f"  Avaliações: {len(m.avaliacoes)} | média: {media:.1f}★" if media else "  Sem avaliações ainda.")

    # --- Compradora ---
    def entrar_compradora(self) -> None:
        c = escolher(self.compradoras, lambda e: f"{e.nome} ({e.localizacao})", "Qual empresa compradora?")
        if not c:
            return
        acoes = {1: lambda: self.c_consultar(c), 2: lambda: self.c_comparar(c),
                 3: lambda: self.c_pedido(c), 4: lambda: self.c_meus_pedidos(c),
                 5: lambda: self.c_avaliar(c)}
        while True:
            op = menu(f"COMPRADORA: {c.nome}", [
                "Consultar produtos (filtros e ordenação)", "Comparar produtos",
                "Realizar pedido", "Meus pedidos", "Avaliar marisqueira",
            ])
            if op == 0:
                return
            self._seguro(acoes[op])

    def c_consultar(self, c: EmpresaCompradora) -> None:
        print("\nFiltros (Enter para ignorar):")
        nome = ler_texto("  Nome do produto: ", obrigatorio=False) or None
        categoria = escolher_categoria()
        localizacao = ler_texto("  Localização: ", obrigatorio=False) or None
        empresa = ler_texto("  Empresa/marisqueira: ", obrigatorio=False) or None
        minima = ler_numero("  Avaliação mínima (1 a 5): ", minimo=1, opcional=True)
        print("  Ordenar por: 1 - menor preço | 2 - maior preço | 3 - melhor avaliação | "
              "4 - proximidade | Enter - sem ordem")
        ordem = {"1": "menor_preco", "2": "maior_preco", "3": "melhor_avaliacao", "4": "proximidade"}.get(
            input("  > ").strip())
        resultado = c.consultar_produtos(self.marisqueiras, nome, categoria, localizacao, empresa, minima, ordem)
        print(f"\n{len(resultado)} produto(s) encontrado(s):")
        for p in resultado:
            print("  " + fmt_produto(p, detalhado=True))

    def _produto_por_id(self, texto: str) -> Produto:
        if not texto.isdigit():
            raise ErroRegraNegocio(f"'{texto}' não é um código de produto válido.")
        for p in self.todos_produtos:
            if p.id_produto == int(texto):
                return p
        raise ErroRegraNegocio(f"Produto {texto} não encontrado.")

    def c_comparar(self, c: EmpresaCompradora) -> None:
        print("\nProdutos disponíveis:")
        for p in self.todos_produtos:
            print("  " + fmt_produto(p, detalhado=True))
        codigos = ler_texto("\nCódigos dos produtos a comparar (separados por espaço): ").split()
        tabela = c.comparar_produtos([self._produto_por_id(x) for x in codigos])
        print("\nComparação (do menor para o maior preço):")
        for t in tabela:
            nota = f"{t['avaliacao']}★" if t["avaliacao"] else "sem avaliações"
            print(f"  {t['produto']} ({t['categoria']}) | {t['empresa']} ({t['localizacao']}) | "
                  f"R$ {t['preco']:.2f}/kg | {kg(t['disponivel_kg'])} | {nota}")

    def c_pedido(self, c: EmpresaCompradora) -> None:
        print("\nProdutos disponíveis:")
        for p in self.todos_produtos:
            print("  " + fmt_produto(p, detalhado=True))
        print("\nMonte o pedido (todos os produtos da MESMA marisqueira; mínimo 25 kg por produto).")
        print("Digite: <código> <quantidade em kg>   (Enter vazio para terminar)")
        itens: list[tuple[Produto, float]] = []
        while True:
            linha = input("  item> ").strip()
            if not linha:
                break
            partes = linha.replace(",", ".").split()
            if len(partes) != 2:
                print("  Formato: <código> <kg>, por exemplo: 1 50")
                continue
            try:
                itens.append((self._produto_por_id(partes[0]), float(partes[1])))
            except (ErroRegraNegocio, ValueError) as erro:
                print(f"  ✖ {erro}")
        if not itens:
            print("  Pedido cancelado: nenhum item.")
            return
        endereco = ler_texto("Endereço de entrega: ")
        tempo = ler_texto("Tempo de entrega (ex.: 2 dias): ")
        pedido = c.realizar_pedido(itens, endereco, tempo)
        print("\n  ✔ Pedido enviado para análise da marisqueira:\n  " + fmt_pedido(pedido))

    def c_meus_pedidos(self, c: EmpresaCompradora) -> None:
        print("\nMeus pedidos:")
        if not c.pedidos:
            print("  Você ainda não fez pedidos.")
        for p in c.pedidos:
            print("  " + fmt_pedido(p))

    def c_avaliar(self, c: EmpresaCompradora) -> None:
        avaliaveis = [p for p in c.pedidos if p.status_pedido == StatusPedido.FINALIZADO and not p.avaliado]
        p = escolher(avaliaveis, fmt_pedido, "Pedidos finalizados ainda não avaliados:")
        if p:
            nota = ler_inteiro("Nota de 1 a 5 estrelas: ", 1, 5)
            c.avaliar_empresa(p, nota)
            print(f"\n  ✔ {p.empresa_marisqueira.nome} avaliada com {nota}★.")


def main() -> None:
    Sistema().executar()
