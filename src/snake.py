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
        # ... (outras direções) ...
        
        self.posicao = (x, y)
        self.corpo.insert(0, self.posicao)
        self.corpo.pop() # Esta linha será modificada pela lógica de crescimento

    def mudar_direcao(self, nova_direcao):
        # ... (código existente) ...
        pass

    def crescer(self):
        """Implementa a lógica de crescimento da cobra."""
        self.tamanho += 1
        # Para fazer o corpo crescer, simplesmente adicionamos um segmento
        # na mesma posição do último. O movimento natural se encarregará de ajustá-lo.
        self.corpo.append(self.corpo[-1])