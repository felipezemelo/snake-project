# features/steps/jogo_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

BASE_URL = "http://127.0.0.1:5000"

# --- Funções de ajuda Refinadas ---

def start_game(context):
    """Inicia um navegador e o jogo, deixando-o pronto para ser manipulado."""
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except Exception:
            pass # Ignora erros se o navegador já estiver fechado
    context.driver = webdriver.Chrome()
    
    context.driver.get(BASE_URL)
    # CORREÇÃO: Passa context.driver em vez de context para o WebDriverWait
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'start-screen'))
    )
    
    body = context.driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.SPACE)
    
    normal_button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'normalBtn'))
    )
    normal_button.click()
    time.sleep(1)

def call_api_sync(context, url, data):
    """Executa uma chamada de API e ESPERA pela sua conclusão."""
    script = f"""
        const callback = arguments[0];
        fetch('{url}', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({json.dumps(data)})
        }}).then(() => callback());
    """
    context.driver.execute_async_script(script)

def get_game_state(context):
    """Usa a API passiva para obter o estado do jogo sem o modificar."""
    return context.driver.execute_script("return await (await fetch('/api/get_current_state')).json()")

# --- Implementação Final de TODOS os Steps ---

# Passos para Pontuação, Power-ups e Tamanho
@given(u'que eu estou em uma partida com pontuação "{pontuacao}" e a cobra tem tamanho "{tamanho}"')
def step_impl(context, pontuacao, tamanho):
    start_game(context)
    call_api_sync(context, '/api/test/set_state', {'score': pontuacao, 'snake_size': tamanho})

@given(u'um "{tipo_rato}" está na célula à frente da cobra')
def step_impl(context, tipo_rato):
    state = get_game_state(context)
    snake_head = state['snake_body'][0]
    food_pos = {'x': snake_head[0] + 1, 'y': snake_head[1]}
    rat_type_map = { "Rato Normal": "NORMAL", "Rato Dourado": "DOURADO", "Rato Vermelho": "VERMELHO" }
    food_type = rat_type_map.get(tipo_rato, "NORMAL")
    call_api_sync(context, '/api/test/set_food', {'x': food_pos['x'], 'y': food_pos['y'], 'type': food_type})

@when(u'a cobra se move e come o "{tipo_rato}"')
def step_impl(context, tipo_rato):
    time.sleep(0.5)

@then(u'minha pontuação deve ser "{pontuacao_final}"')
def step_impl(context, pontuacao_final):
    state = get_game_state(context)
    assert state['score'] == int(pontuacao_final)

@then(u'o tamanho da cobra deve ser "{tamanho_final}"')
def step_impl(context, tamanho_final):
    state = get_game_state(context)
    assert len(state['snake_body']) == int(tamanho_final)
    context.driver.quit()

# Passos para Fim de Jogo e Colisão
@given(u'que a cobra está na borda superior do cenário e se movendo para "cima"')
def step_impl(context):
    start_game(context)
    call_api_sync(context, '/api/test/set_snake', {'body': [[10, 0], [10, 1]], 'direction': 'CIMA'})

@when(u'a cobra tenta se mover mais uma vez')
def step_impl(context):
    time.sleep(0.5)

@then(u'a tela de "Game Over" deve ser exibida')
def step_impl(context):
    game_over_screen = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'game-over-screen'))
    )
    assert "visible" in game_over_screen.get_attribute('class')
    context.driver.quit()

@given(u'que a cobra tem tamanho "{tamanho}" e está prestes a cruzar seu próprio corpo')
def step_impl(context, tamanho):
    start_game(context)
    colliding_body = [[5, 5], [6, 5], [7, 5], [7, 6], [6, 6]]
    call_api_sync(context, '/api/test/set_snake', {'body': colliding_body, 'direction': 'ESQUERDA'})

@when(u'a cobra se move')
def step_impl(context):
    time.sleep(0.5)

# Passos para Visualização de Pontuação Final
@given(u'que eu terminei uma partida com "{pontos}" pontos')
def step_impl(context, pontos):
    start_game(context)
    call_api_sync(context, '/api/test/set_state', {'score': pontos})
    call_api_sync(context, '/api/test/set_snake', {'body': [[-1, 10]]})

@when(u'a tela de "Game Over" é exibida')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'game-over-screen'))
    )

@then(u'o texto "Pontuação Final: {pontos}" deve estar visível na tela')
def step_impl(context, pontos):
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, 'finalScore'), pontos)
    )
    final_score_element = context.driver.find_element(By.ID, 'finalScore')
    assert final_score_element.text == pontos
    context.driver.quit()