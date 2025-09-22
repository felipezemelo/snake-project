# features/steps/controlar_cobra_steps.py
from behave import given, when, then

@given(u'que o jogo começou e a cobra está se movendo para a direita')
def step_impl(context):
    # Aqui entrará o código para iniciar o jogo e verificar a direção inicial
    raise NotImplementedError(u'STEP: Given que o jogo começou e a cobra está se movendo para a direita')

@when(u'eu aperto a tecla "seta para cima"')
def step_impl(context):
    # Código com Selenium para simular o pressionamento da tecla
    raise NotImplementedError(u'STEP: When eu aperto a tecla "seta para cima"')

@then(u'a direção da cobra deve mudar para "cima"')
def step_impl(context):
    # Código para verificar a mudança de estado/direção da cobra no jogo
    raise NotImplementedError(u'STEP: Then a direção da cobra deve mudar para "cima"')