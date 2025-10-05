# src/snake.py
class Snake:
    def __init__(self):
        self.tamanho = 3
        self.posicao = (10, 10)
        self.direcao = "DIREITA"
        self.corpo = [(10, 10), (9, 10), (8, 10)]

    def mover(self):
        x, y = self.posicao
        if self.direcao == "DIREITA": x += 1
        elif self.direcao == "ESQUERDA": x -= 1
        elif self.direcao == "CIMA": y -= 1
        elif self.direcao == "BAIXO": y += 1
        self.posicao = (x, y)
        self.corpo.insert(0, self.posicao)
        self.corpo.pop()

    def mudar_direcao(self, nova_direcao):
        if (nova_direcao == "CIMA" and self.direcao != "BAIXO") or \
           (nova_direcao == "BAIXO" and self.direcao != "CIMA") or \
           (nova_direcao == "ESQUERDA" and self.direcao != "DIREITA") or \
           (nova_direcao == "DIREITA" and self.direcao != "ESQUERDA"):
            self.direcao = nova_direcao

    def crescer(self):
        self.tamanho += 1
        self.corpo.append(self.corpo[-1])

    def encolher(self):
        """Implementa a lógica de encolhimento da cobra."""
        if len(self.corpo) > 3:
            self.corpo.pop()
            self.tamanho -= 1

    def verificar_colisao(self, largura_grid, altura_grid):
        x, y = self.posicao
        if x < 0 or x >= largura_grid or y < 0 or y >= altura_grid:
            return True
        if self.posicao in self.corpo[1:]:
            return True
        return False