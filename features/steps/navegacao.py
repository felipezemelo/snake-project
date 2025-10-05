# features/steps/navegacao_steps.py
from behave import given, when, then

# Passos de Iniciar Partida
@given('que eu estou na tela inicial do jogo')
def step_impl(context):
    pass # Este já está implementado

@when('eu aperto qualquer tecla')
def step_impl(context):
    pass # Este já está implementado

@then('a tela de seleção de dificuldade deve ser exibida')
def step_impl(context):
    pass # Este já está implementado

# Passos de Selecionar Dificuldade (já implementados no seu `dificuldade_steps.py`)
# Mova a lógica do seu `dificuldade_steps.py` para cá se quiser consolidar.
# Por enquanto, vamos manter os arquivos separados.