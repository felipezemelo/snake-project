# src/board.py
import random

class Food:
    """Representa a comida no jogo, agora com um tipo."""
    def __init__(self, x, y, food_type='NORMAL'):
        self.posicao = (x, y)
        self.type = food_type

class Board:
    """Representa o tabuleiro do jogo, suas dimensões e a comida."""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.comida = None

    def gerar_comida(self, corpo_cobra):
        """Cria um novo objeto de comida numa posição aleatória que não esteja ocupada pela cobra."""
        while True:
            x = random.randint(0, self.largura - 1)
            y = random.randint(0, self.altura - 1)
            posicao_potencial = (x, y)
            
            if posicao_potencial not in corpo_cobra:
                # Altera as probabilidades: Rato Vermelho agora é mais raro (5%)
                tipos_de_comida = ['NORMAL', 'DOURADO', 'VERMELHO']
                probabilidades = [0.85, 0.10, 0.05] # 85% Normal, 10% Dourado, 5% Vermelho
                tipo_escolhido = random.choices(tipos_de_comida, probabilidades, k=1)[0]
                self.comida = Food(x, y, food_type=tipo_escolhido)
                break