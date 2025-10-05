# tests/test_game.py
import pytest
from src.game import Game
from src.board import Board, Food
from src.snake import Snake

def test_inicio_do_jogo_cria_instancias_corretas():
    """Testa se o jogo começa com um tabuleiro e uma cobra."""
    jogo = Game(largura=20, altura=20)
    assert isinstance(jogo.board, Board)
    assert isinstance(jogo.snake, Snake)
    assert jogo.pontuacao == 0
    assert jogo.game_over == False

def test_cobra_come_comida():
    """Testa o que acontece quando a cobra come a comida."""
    jogo = Game(largura=20, altura=20)
    tamanho_inicial_cobra = jogo.snake.tamanho
    pontuacao_inicial = jogo.pontuacao

    # Força a posição da comida para o local onde a cobra ESTARÁ
    # A cobra começa em (10, 10) e se move para a DIREITA. A próxima posição será (11, 10).
    jogo.board.comida.posicao = (11, 10)
    posicao_comida_antiga = jogo.board.comida.posicao
    
    jogo.update()

    assert jogo.snake.tamanho == tamanho_inicial_cobra + 1
    assert jogo.pontuacao > pontuacao_inicial
    assert jogo.board.comida.posicao != posicao_comida_antiga

def test_game_over_por_colisao_com_parede():
    """Testa se o jogo termina quando a cobra colide com a parede."""
    jogo = Game(largura=20, altura=20)
    # Força a cobra para a borda e a move em direção à parede
    jogo.snake.posicao = (19, 10)
    jogo.snake.direcao = "DIREITA"
    jogo.snake.corpo = [(19, 10), (18, 10), (17, 10)]

    jogo.update()
    
    assert jogo.game_over == True

def test_cobra_come_rato_dourado_e_ganha_mais_pontos():
    """Testa o efeito do power-up do rato dourado."""
    jogo = Game(largura=20, altura=20)
    pontuacao_inicial = jogo.pontuacao
    
    # Força a criação de um rato dourado na posição em que a cobra vai estar
    posicao_futura_cobra = (jogo.snake.posicao[0] + 1, jogo.snake.posicao[1])
    jogo.board.comida = Food(posicao_futura_cobra[0], posicao_futura_cobra[1], food_type='DOURADO')
    
    jogo.update()

    assert jogo.pontuacao == pontuacao_inicial + 25

def test_cobra_come_rato_vermelho_e_encolhe():
    """Testa o efeito do power-up do rato vermelho."""
    jogo = Game(largura=20, altura=20)

    # Faz a cobra crescer para ter mais de 10 segmentos
    for _ in range(8):
        jogo.snake.crescer()

    tamanho_inicial = jogo.snake.tamanho # Será 11
    segmentos_a_remover = tamanho_inicial // 2
    tamanho_esperado = tamanho_inicial - segmentos_a_remover # CORRIGIDO AQUI

    # Força a criação de um rato vermelho na posição em que a cobra vai estar
    posicao_futura_cobra = (jogo.snake.posicao[0] + 1, jogo.snake.posicao[1])
    jogo.board.comida = Food(posicao_futura_cobra[0], posicao_futura_cobra[1], food_type='VERMELHO')

    jogo.update()
    
    assert jogo.snake.tamanho == tamanho_esperado