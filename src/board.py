# src/board.py
import random

class Food:
    """Representa a comida (Rato Cinza) no jogo."""
    def __init__(self, x, y):
        self.posicao = (x, y)

class Board:
    """Representa o tabuleiro do jogo, suas dimensões e a comida."""

    def __init__(self, largura, altura):
        """Inicializa o tabuleiro com a largura e altura especificadas."""
        self.largura = largura
        self.altura = altura
        self.comida = None
        self.gerar_comida()

    def gerar_comida(self):
        """Cria um novo objeto de comida em uma posição aleatória dentro do tabuleiro."""
        x = random.randint(0, self.largura - 1)
        y = random.randint(0, self.altura - 1)
        self.comida = Food(x, y)