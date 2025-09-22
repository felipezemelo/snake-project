# features/steps/pontuacao_e_crescimento_steps.py
from behave import given, when, then

@given(u'que eu estou em uma partida com pontuação "50" e a cobra tem tamanho "10"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given que eu estou em uma partida com pontuação "50" e a cobra tem tamanho "10"')

@given(u'um "Rato Cinza" está na célula à frente da cobra')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given um "Rato Cinza" está na célula à frente da cobra')

@when(u'a cobra se move e come o "Rato Cinza"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When a cobra se move e come o "Rato Cinza"')

@then(u'minha pontuação deve ser "55"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then minha pontuação deve ser "55"')

@then(u'o tamanho da cobra deve ser "11"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then o tamanho da cobra deve ser "11"')