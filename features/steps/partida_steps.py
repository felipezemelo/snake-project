# Importa os "decoradores" do behave que fazem a ligação com o Gherkin
from behave import given, when, then

# A frase dentro do @given() deve ser EXATAMENTE IGUAL à frase no arquivo .feature
@given('que eu estou na tela inicial do jogo')
def step_impl(context):
    # 'pass' significa que por enquanto não faremos nada, mas o teste é reconhecido.
    # Aqui entrará o código do Selenium para abrir o navegador.
    pass

@when('eu aperto qualquer tecla')
def step_impl(context):
    # Aqui entrará o código do Selenium para simular o pressionar de uma tecla.
    pass

@then('a tela de seleção de dificuldade deve ser exibida')
def step_impl(context):
    # Aqui entrará o código do Selenium para verificar se a nova tela apareceu.
    pass