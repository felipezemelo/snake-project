# features/steps/visualizar_pontuacao_final_steps.py
from behave import given, when, then

@given(u'que eu terminei uma partida com "150" pontos')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given que eu terminei uma partida com "150" pontos')

@when(u'a tela de "Game Over" é exibida')
def step_impl(context):
    raise NotImplementedError(u'STEP: When a tela de "Game Over" é exibida')

@then(u'o texto "Pontuação Final: 150" deve estar visível na tela')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then o texto "Pontuação Final: 150" deve estar visível na tela')