# src/board.py
import random

class Food:
    """Representa a comida no jogo, agora com um tipo."""
    def __init__(self, x, y, food_type='NORMAL'):
        self.posicao = (x, y)
        self.type = food_type # Ex: 'NORMAL', 'DOURADO', 'VERMELHO'

class Board:
    """Representa o tabuleiro do jogo, suas dimensões e a comida."""

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.comida = None
        # A geração inicial é tratada pelo Game __init__ agora

    def gerar_comida(self, corpo_cobra):
        """Cria um novo objeto de comida numa posição aleatória que não esteja ocupada pela cobra."""
        while True:
            x = random.randint(0, self.largura - 1)
            y = random.randint(0, self.altura - 1)
            posicao_potencial = (x, y)
            
            if posicao_potencial not in corpo_cobra:
                # 80% de chance de ser Normal, 10% Dourado, 10% Vermelho
                tipos_de_comida = ['NORMAL', 'DOURADO', 'VERMELHO']
                probabilidades = [0.8, 0.1, 0.1]
                tipo_escolhido = random.choices(tipos_de_comida, probabilidades, k=1)[0]
                self.comida = Food(x, y, food_type=tipo_escolhido)
                break