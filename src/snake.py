class Snake:
    """Representa a cobra no jogo."""

    def __init__(self):
        """Inicializa a cobra com valores padrão."""
        # Define um tamanho inicial para a cobra
        self.tamanho = 3
        # Define a posição inicial da cabeça da cobra no centro de um grid imaginário
        self.posicao = (10, 10) 
        # Define a direção inicial do movimento
        self.direcao = "DIREITA"
        # O corpo pode ser uma lista de coordenadas
        self.corpo = [(10, 10), (9, 10), (8, 10)]

    def mover(self):
        """Implementa a lógica de movimento da cobra."""
        # A lógica de movimento será adicionada aqui em um próximo passo do TDD.
        pass

    def crescer(self):
        """Implementa a lógica de crescimento da cobra."""
        # A lógica de crescimento será adicionada aqui.
        pass