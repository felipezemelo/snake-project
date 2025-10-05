# features/steps/controlar_cobra_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://127.0.0.1:5000"

@given(u'que o jogo começou e a cobra está se movendo para a "{direcao}"')
def step_impl(context, direcao):
    # 1. Inicia o navegador e o jogo
    context.driver = webdriver.Chrome()
    context.driver.get(BASE_URL)
    time.sleep(1)

    body = context.driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.SPACE)
    time.sleep(1)
    context.driver.find_element(By.ID, 'normalBtn').click()
    time.sleep(1)
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Se a direção inicial pedida pelo teste não for 'direita' (o padrão),
    # nós simulamos a tecla necessária para chegar a essa direção.
    if direcao.lower() == "cima":
        body.send_keys(Keys.ARROW_UP)
        time.sleep(0.5) # Dá tempo para o jogo processar a mudança de direção

@when(u'eu aperto a tecla "{tecla}"')
def step_impl(context, tecla):
    body = context.driver.find_element(By.TAG_NAME, 'body')
    key_map = {
        "seta para cima": Keys.ARROW_UP,
        "seta para baixo": Keys.ARROW_DOWN,
        "seta para esquerda": Keys.ARROW_LEFT,
        "seta para direita": Keys.ARROW_RIGHT,
    }
    if tecla in key_map:
        body.send_keys(key_map[tecla])
        time.sleep(0.5)

@then(u'a direção da cobra deve mudar para "{direcao_esperada}"')
def step_impl(context, direcao_esperada):
    game_state = context.driver.execute_script("return await (await fetch('/api/state')).json()")
    assert game_state['snake_direction'] == direcao_esperada.upper()
    context.driver.quit()

@then(u'a direção da cobra deve continuar sendo "{direcao_esperada}"')
def step_impl(context, direcao_esperada):
    game_state = context.driver.execute_script("return await (await fetch('/api/state')).json()")
    assert game_state['snake_direction'] == direcao_esperada.upper()
    context.driver.quit()