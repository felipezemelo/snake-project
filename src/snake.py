# src/snake.py

class Snake:
    def __init__(self):
        """Inicializa a cobra com valores padrão."""
        self.tamanho = 3
        self.posicao = (10, 10)
        self.direcao = "DIREITA"
        self.corpo = [(10, 10), (9, 10), (8, 10)]

    def mover(self):
        """Implementa a lógica de movimento da cobra."""
        x, y = self.posicao
        if self.direcao == "DIREITA":
            x += 1
        elif self.direcao == "ESQUERDA":
            x -= 1
        elif self.direcao == "CIMA":
            y -= 1
        elif self.direcao == "BAIXO":
            y += 1
        
        self.posicao = (x, y)
        self.corpo.insert(0, self.posicao)
        self.corpo.pop()

    def mudar_direcao(self, nova_direcao):
        """Altera a direção da cobra, impedindo que ela se mova para trás."""
        if nova_direcao == "CIMA" and self.direcao != "BAIXO":
            self.direcao = nova_direcao
        elif nova_direcao == "BAIXO" and self.direcao != "CIMA":
            self.direcao = nova_direcao
        elif nova_direcao == "ESQUERDA" and self.direcao != "DIREITA":
            self.direcao = nova_direcao
        elif nova_direcao == "DIREITA" and self.direcao != "ESQUERDA":
            self.direcao = nova_direcao

    def crescer(self):
        """Implementa a lógica de crescimento da cobra."""
        self.tamanho += 1
        self.corpo.append(self.corpo[-1])

    def verificar_colisao(self, largura_grid, altura_grid):
        """
        Verifica se a cobra colidiu com as paredes ou com o próprio corpo.
        Retorna True se houver colisão, False caso contrário.
        """
        x, y = self.posicao
        
        # 1. Colisão com as paredes
        if x < 0 or x >= largura_grid or y < 0 or y >= altura_grid:
            return True
            
        # 2. Colisão com o próprio corpo
        if self.posicao in self.corpo[1:]:
            return True
            
        return False