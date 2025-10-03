# tests/test_game.py
import pytest
from src.game import Game
from src.board import Board
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

    # Força a posição da cobra para ser a mesma da comida no tabuleiro
    jogo.snake.posicao = jogo.board.comida.posicao
    posicao_comida_antiga = jogo.board.comida.posicao
    
    jogo.update()

    assert jogo.snake.tamanho == tamanho_inicial_cobra + 1
    assert jogo.pontuacao > pontuacao_inicial
    # Verifica se o tabuleiro gerou uma nova comida em um local diferente
    assert jogo.board.comida.posicao != posicao_comida_antiga

def test_game_over_por_colisao_com_parede():
    """Testa se o jogo termina quando a cobra colide com a parede."""
    jogo = Game(largura=20, altura=20)
    # Força a cobra a uma posição de colisão
    jogo.snake.posicao = (-1, 10)
    
    jogo.update()
    
    assert jogo.game_over == True