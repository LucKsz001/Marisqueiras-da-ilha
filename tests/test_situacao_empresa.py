from datetime import time

from marisqueiras_da_ilha import Categoria, EmpresaMarisqueira, SituacaoEmpresa


def test_verde_quando_disponivel(maria, sururu):
    assert maria.situacao(time(10, 0)) == SituacaoEmpresa.DISPONIVEL


def test_laranja_com_estoque_baixo(maria):
    maria.cadastrar_produto("Sururu", Categoria.FRESCO, 30.0, 40)
    assert maria.situacao(time(10, 0)) == SituacaoEmpresa.ESTOQUE_BAIXO


def test_vermelho_fora_do_horario(maria, sururu):
    assert maria.situacao(time(23, 0)) == SituacaoEmpresa.FORA_DO_HORARIO
    assert maria.situacao(time(5, 59)) == SituacaoEmpresa.FORA_DO_HORARIO


def test_horarios_limite_estao_dentro_do_funcionamento(maria, sururu):
    assert maria.situacao(time(6, 0)) == SituacaoEmpresa.DISPONIVEL
    assert maria.situacao(time(18, 0)) == SituacaoEmpresa.DISPONIVEL


def test_empresa_sem_estoque_continua_cadastrada(maria, sururu):
    maria.alterar_quantidade(sururu, 0)
    assert sururu in maria.produtos
    assert maria.situacao(time(10, 0)) == SituacaoEmpresa.ESTOQUE_BAIXO


def test_horario_personalizado():
    m = EmpresaMarisqueira("11222333000181", "M", "Vila", abertura=time(8, 0), fechamento=time(12, 0))
    assert m.situacao(time(13, 0)) == SituacaoEmpresa.FORA_DO_HORARIO
