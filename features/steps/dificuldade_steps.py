# Não esqueça de adicionar esta linha no topo do novo arquivo
from behave import given, when, then

@given(u'que eu estou na tela de seleção de dificuldade')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given que eu estou na tela de seleção de dificuldade')

@when(u'eu seleciono a opção "Normal"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When eu seleciono a opção "Normal"')

@then(u'o jogo deve iniciar no modo Normal')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then o jogo deve iniciar no modo Normal')

@when(u'eu seleciono a opção "Difícil"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When eu seleciono a opção "Difícil"')

@then(u'o jogo deve iniciar no modo Difícil')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then o jogo deve iniciar no modo Difícil')