# features/steps/dificuldade_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://127.0.0.1:5000"

@given('que eu estou na tela de seleção de dificuldade')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get(BASE_URL)
    time.sleep(1)
    # Simula o passo anterior para chegar à tela de dificuldade
    body = context.driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.SPACE)
    time.sleep(1)
    difficulty_screen = context.driver.find_element(By.ID, 'difficulty-screen')
    assert difficulty_screen.is_displayed()

@when('eu seleciono a opção "Normal"')
def step_impl(context):
    normal_button = context.driver.find_element(By.ID, 'normalBtn')
    normal_button.click()
    time.sleep(1) # Espera o jogo começar

@then('o jogo deve iniciar no modo Normal')
def step_impl(context):
    # Uma forma de verificar se o jogo iniciou é ver se a tela de dificuldade desapareceu
    difficulty_screen = context.driver.find_element(By.ID, 'difficulty-screen')
    assert not difficulty_screen.is_displayed()
    context.driver.quit()

# --- Cenário para o modo Difícil ---

@when('eu seleciono a opção "Difícil"')
def step_impl(context):
    hard_button = context.driver.find_element(By.ID, 'dificilBtn')
    hard_button.click()
    time.sleep(1)

@then('o jogo deve iniciar no modo Difícil')
def step_impl(context):
    difficulty_screen = context.driver.find_element(By.ID, 'difficulty-screen')
    assert not difficulty_screen.is_displayed()
    context.driver.quit()