# src/game.py
from src.snake import Snake
from src.board import Board

class Game:
    def __init__(self, largura, altura):
        self.board = Board(largura, altura)
        self.snake = Snake()
        self.pontuacao = 0
        self.game_over = False
        self.board.gerar_comida(self.snake.corpo)

    def update(self):
        if self.game_over:
            return

        self.snake.mover()

        if self.snake.verificar_colisao(self.board.largura, self.board.altura):
            self.game_over = True
            return

        if self.snake.posicao == self.board.comida.posicao:
            tipo_comida = self.board.comida.type
            
            if tipo_comida == 'NORMAL':
                self.snake.crescer()
                self.pontuacao += 5
            elif tipo_comida == 'DOURADO':
                self.snake.crescer()
                self.pontuacao += 25
            elif tipo_comida == 'VERMELHO':
                # --- NOVA LÓGICA DO RATO VERMELHO ---
                # Condição: Só encolhe se a cobra for maior que 10 segmentos
                if self.snake.tamanho > 10:
                    segmentos_a_remover = self.snake.tamanho // 2
                    for _ in range(segmentos_a_remover):
                        self.snake.encolher()
                
                self.pontuacao += 1 # Ganha apenas 1 ponto
            
            self.board.gerar_comida(self.snake.corpo)