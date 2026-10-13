def test_quantidade_igual_ao_estoque_esta_disponivel(sururu):
    assert sururu.verificar_disponibilidade(200)


def test_quantidade_acima_do_estoque_nao_esta_disponivel(sururu):
    assert not sururu.verificar_disponibilidade(200.1)


def test_sem_argumento_usa_minimo_de_25kg(sururu):
    assert sururu.verificar_disponibilidade()
    sururu.atualizar_quantidade(24)
    assert not sururu.verificar_disponibilidade()


def test_estoque_zero_nunca_esta_disponivel(sururu):
    sururu.atualizar_quantidade(0)
    assert not sururu.verificar_disponibilidade(25)
