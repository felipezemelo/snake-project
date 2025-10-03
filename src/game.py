# src/game.py
from src.snake import Snake
from src.board import Board

class Game:
    """Gerencia o fluxo do jogo, unindo o Tabuleiro e a Cobra."""

    def __init__(self, largura, altura):
        """Inicializa o jogo, criando um tabuleiro e uma cobra."""
        self.board = Board(largura, altura)
        self.snake = Snake()
        self.pontuacao = 0
        self.game_over = False

    def update(self):
        """
        Atualiza o estado do jogo em um "tick", verificando o estado atual
        antes de mover a cobra para o próximo estado.
        """
        if self.game_over:
            return

        # 1. Primeiro, verificamos se a posição ATUAL da cobra já é uma colisão.
        if self.snake.verificar_colisao(self.board.largura, self.board.altura):
            self.game_over = True
            return

        # 2. Em seguida, verificamos se a cobra comeu na posição ATUAL.
        if self.snake.posicao == self.board.comida.posicao:
            self.snake.crescer()
            self.pontuacao += 5
            self.board.gerar_comida() # Delega a geração de comida para o tabuleiro

        # 3. Por último, movemos a cobra para a próxima posição.
        self.snake.mover()