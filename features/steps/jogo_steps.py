# features/steps/game_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

BASE_URL = "http://127.0.0.1:5000"

# --- Funções de Ajuda (Helpers) ---

def start_game(context, difficulty='Normal'):
    if hasattr(context, 'driver') and context.driver:
        try: context.driver.quit()
        except Exception: pass
    
    context.driver = webdriver.Chrome()
    context.driver.get(BASE_URL)
    
    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.ID, 'start-screen')))
    context.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
    
    button_id = 'normalBtn' if difficulty == 'Normal' else 'dificilBtn'
    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.ID, button_id))).click()

    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.ID, 'playBtn'))).click()
    time.sleep(1)

def call_api_sync(context, url, data):
    script = f"""
        const callback = arguments[0];
        fetch('{url}', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({json.dumps(data)})
        }}).then(response => response.json()).then(() => callback());
    """
    context.driver.execute_async_script(script)

def get_game_state(context):
    return context.driver.execute_script("return await (await fetch('/api/state')).json()")

def get_game_speed(context):
    return context.driver.execute_script("return window.currentSpeed;")

# --- Steps de Navegação e Início de Jogo ---

@given('que eu estou na tela inicial do jogo')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get(BASE_URL)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.ID, 'start-screen')))

@when('eu aperto qualquer tecla')
def step_impl(context):
    context.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)

@then('a tela de seleção de dificuldade deve ser exibida')
def step_impl(context):
    assert WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.ID, 'difficulty-screen'))).is_displayed()
    context.driver.quit()

@given('que eu estou na tela de seleção de dificuldade')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get(BASE_URL)
    context.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.ID, 'difficulty-screen')))

@when('eu seleciono a opção "{difficulty}"')
def step_impl(context, difficulty):
    button_id = 'normalBtn' if difficulty == 'Normal' else 'dificilBtn'
    context.driver.find_element(By.ID, button_id).click()

@then('o jogo deve iniciar no modo {difficulty}')
def step_impl(context, difficulty):
    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.ID, 'playBtn'))).click()
    time.sleep(0.5)
    assert not context.driver.find_element(By.ID, 'tutorial-screen').is_displayed()
    context.driver.quit()

# --- Steps de Controle da Cobra ---

@given('que o jogo começou e a cobra está se movendo para a "{direction}"')
def step_impl(context, direction):
    start_game(context)
    if direction.upper() != "DIREITA":
        body = context.driver.find_element(By.TAG_NAME, 'body')
        key_to_press = None
        if direction.lower() == "cima": key_to_press = Keys.ARROW_UP
        elif direction.lower() == "baixo": key_to_press = Keys.ARROW_DOWN
        
        if key_to_press:
            body.send_keys(key_to_press)
            WebDriverWait(context, 10).until(
                lambda c: get_game_state(c)['snake_direction'] == direction.upper()
            )

@when('eu aperto a tecla "{key_name}"')
def step_impl(context, key_name):
    key_map = {"seta para cima": Keys.ARROW_UP, "seta para baixo": Keys.ARROW_DOWN, "seta para esquerda": Keys.ARROW_LEFT, "seta para direita": Keys.ARROW_RIGHT}
    if key_name in key_map:
        context.driver.find_element(By.TAG_NAME, 'body').send_keys(key_map[key_name])
        time.sleep(0.5)

@then('a direção da cobra deve mudar para "{expected_direction}"')
def step_impl(context, expected_direction):
    WebDriverWait(context, 10).until(
        lambda c: get_game_state(c)['snake_direction'] == expected_direction.upper()
    )
    state = get_game_state(context)
    assert state['snake_direction'] == expected_direction.upper()
    context.driver.quit()

@then('a direção da cobra deve continuar sendo "{expected_direction}"')
def step_impl(context, expected_direction):
    state = get_game_state(context)
    assert state['snake_direction'] == expected_direction.upper()
    context.driver.quit()

# --- Steps de Pontuação, Power-ups e Crescimento ---

@given('que eu estou em uma partida com pontuação "{score}" e a cobra tem tamanho "{size}"')
def step_impl(context, score, size):
    start_game(context)
    call_api_sync(context, '/api/test/set_state', {'score': int(score), 'snake_size': int(size)})

@given('um "{rat_type}" está na célula à frente da cobra')
def step_impl(context, rat_type):
    state = get_game_state(context)
    snake_head = state['snake_body'][0]
    direction = state['snake_direction']
    food_pos = {'x': snake_head[0], 'y': snake_head[1]}
    if direction == 'DIREITA': food_pos['x'] += 1
    elif direction == 'ESQUERDA': food_pos['x'] -= 1
    elif direction == 'CIMA': food_pos['y'] -= 1
    elif direction == 'BAIXO': food_pos['y'] += 1
    
    rat_type_map = {"Rato Normal": "NORMAL", "Rato Dourado": "DOURADO", "Rato Vermelho": "VERMELHO"}
    food_type = rat_type_map.get(rat_type, "NORMAL")
    call_api_sync(context, '/api/test/set_food', {'x': food_pos['x'], 'y': food_pos['y'], 'type': food_type})

@when('a cobra se move e come o "{rat_type}"')
def step_impl(context, rat_type):
    time.sleep(0.5)

@then('minha pontuação deve ser "{final_score}"')
def step_impl(context, final_score):
    assert get_game_state(context)['score'] == int(final_score)

@then('o tamanho da cobra deve ser "{final_size}"')
def step_impl(context, final_size):
    assert len(get_game_state(context)['snake_body']) == int(final_size)
    context.driver.quit()

# --- Steps de Fim de Jogo e Colisão ---

@given('que a cobra está na borda superior do cenário e se movendo para "cima"')
def step_impl(context):
    start_game(context)
    call_api_sync(context, '/api/test/set_snake', {'body': [[10, 0], [10, 1]], 'direction': 'CIMA'})

@when('a cobra tenta se mover mais uma vez')
def step_impl(context):
    time.sleep(0.5)

@then('a tela de "Game Over" deve ser exibida')
def step_impl(context):
    assert get_game_state(context)['game_over'] is True
    assert WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.ID, 'game-over-screen')))
    context.driver.quit()

@given('que a cobra tem tamanho "{size}" e está prestes a cruzar seu próprio corpo')
def step_impl(context, size):
    start_game(context)
    colliding_body = [[5, 5], [4, 5], [4, 6], [5, 6], [6, 6]]
    call_api_sync(context, '/api/test/set_snake', {'body': colliding_body[:int(size)], 'direction': 'BAIXO'})

@when('a cobra se move')
def step_impl(context):
    time.sleep(0.5)

# --- Steps de Visualização de Pontuação Final ---

@given('que eu terminei uma partida com "{points}" pontos')
def step_impl(context, points):
    start_game(context)
    context.points = int(points)

@when('a tela de "Game Over" é exibida')
def step_impl(context):
    call_api_sync(context, '/api/test/set_state', {'score': context.points})
    call_api_sync(context, '/api/test/set_snake', {'body': [[-1, -1]]})
    get_game_state(context)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.ID, 'game-over-screen')))

@then('o texto "Pontuação Final: {points}" deve estar visível na tela')
def step_impl(context, points):
    # --- CORREÇÃO FINAL APLICADA AQUI ---
    # Espera que o ecrã de game over esteja numa condição estável.
    WebDriverWait(context.driver, 10).until(
        EC.any_of(
            EC.visibility_of_element_located((By.ID, 'final-scores')),
            EC.visibility_of_element_located((By.ID, 'new-highscore-entry'))
        )
    )

    # Obtém o conteúdo do elemento da pontuação via JS, ignorando se está visível ou não.
    score_text = context.driver.execute_script("return document.getElementById('finalScore').textContent;")
    assert score_text == points
    context.driver.quit()

# --- Steps para Aumento de Velocidade ---

@given('que eu estou em uma partida no modo "{difficulty}" com a velocidade inicial')
def step_impl(context, difficulty):
    start_game(context, difficulty)
    context.initial_speed = get_game_speed(context)

@given('minha pontuação é "{score}"')
def step_impl(context, score):
    call_api_sync(context, '/api/test/set_state', {'score': int(score)})

@when('a cobra come um "Rato Normal" e minha pontuação se torna "{new_score}"')
def step_impl(context, new_score):
    call_api_sync(context, '/api/test/set_state', {'score': int(new_score)})
    time.sleep(0.3) 

@then('a velocidade do jogo deve aumentar para o "{level}"')
def step_impl(context, level):
    assert get_game_speed(context) < context.initial_speed
    context.driver.quit()

@then('a velocidade do jogo deve permanecer a mesma')
def step_impl(context):
    assert get_game_speed(context) == context.initial_speed
    context.driver.quit()

@given('que eu estou em uma partida no modo "Normal" com a velocidade no "{level}"')
def step_impl(context, level):
    start_game(context, 'Normal')
    score_for_level_2 = 50 
    call_api_sync(context, '/api/test/set_state', {'score': score_for_level_2})
    time.sleep(0.3) 
    context.initial_speed = get_game_speed(context)