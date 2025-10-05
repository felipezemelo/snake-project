# tests/test_board.py
import pytest
from src.board import Board, Food

def test_cria_tabuleiro_com_dimensoes_corretas():
    """Testa se o tabuleiro é inicializado com a largura e altura corretas."""
    tabuleiro = Board(largura=25, altura=30)
    assert tabuleiro.largura == 25
    assert tabuleiro.altura == 30

def test_gerar_comida_cria_instancia_de_food():
    """Testa se a comida gerada é um objeto da classe Food."""
    tabuleiro = Board(largura=20, altura=20)
    # É preciso chamar gerar_comida para que o atributo 'comida' seja inicializado.
    # Passamos um corpo de cobra fictício como argumento.
    tabuleiro.gerar_comida(corpo_cobra=[(0,0)])
    assert isinstance(tabuleiro.comida, Food)

def test_gerar_comida_dentro_dos_limites():
    """Testa se a comida gerada está dentro dos limites do tabuleiro."""
    tabuleiro = Board(largura=20, altura=20)
    
    # Roda a geração de comida várias vezes para garantir aleatoriedade
    for _ in range(100):
        # O método requer o argumento 'corpo_cobra'.
        tabuleiro.gerar_comida(corpo_cobra=[(0,0)])
        comida_x, comida_y = tabuleiro.comida.posicao
        assert 0 <= comida_x < tabuleiro.largura
        assert 0 <= comida_y < tabuleiro.altura