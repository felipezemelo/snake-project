# tests/test_snake.py
import pytest
from src.snake import Snake

def test_mover_serpente_para_direita():
    """Testa se a cobra se move corretamente para a direita."""
    serpente = Snake()
    serpente.direcao = "DIREITA"
    posicao_inicial = serpente.posicao
    serpente.mover()
    assert serpente.posicao == (posicao_inicial[0] + 1, posicao_inicial[1])

def test_mover_serpente_para_esquerda():
    """Testa se a cobra se move corretamente para a esquerda."""
    serpente = Snake()
    serpente.direcao = "ESQUERDA"
    posicao_inicial = serpente.posicao
    serpente.mover()
    assert serpente.posicao == (posicao_inicial[0] - 1, posicao_inicial[1])

def test_mover_serpente_para_cima():
    """Testa se a cobra se move corretamente para cima."""
    serpente = Snake()
    serpente.direcao = "CIMA"
    posicao_inicial = serpente.posicao
    serpente.mover()
    assert serpente.posicao == (posicao_inicial[0], posicao_inicial[1] - 1)

def test_mover_serpente_para_baixo():
    """Testa se a cobra se move corretamente para baixo."""
    serpente = Snake()
    serpente.direcao = "BAIXO"
    posicao_inicial = serpente.posicao
    serpente.mover()
    assert serpente.posicao == (posicao_inicial[0], posicao_inicial[1] + 1)

def test_crescimento_da_cobra():
    """Testa se a cobra aumenta de tamanho e o corpo cresce."""
    # Configuração
    serpente = Snake()
    tamanho_inicial = serpente.tamanho
    comprimento_corpo_inicial = len(serpente.corpo)

    # Ação
    serpente.crescer()

    # Verificação
    assert serpente.tamanho == tamanho_inicial + 1
    assert len(serpente.corpo) == comprimento_corpo_inicial + 1


# --- Testes de Colisão ---

def test_colisao_com_parede_superior():
    """Testa se a colisão com a parede superior (y < 0) é detectada."""
    serpente = Snake()
    serpente.posicao = (10, -1) # Posição inválida, acima do limite
    # Assumindo um grid de 20x20, a colisão deve ser True
    assert serpente.verificar_colisao(20, 20) == True

def test_colisao_com_parede_direita():
    """Testa se a colisão com a parede direita (x >= largura_grid) é detectada."""
    serpente = Snake()
    serpente.posicao = (20, 10) # Posição inválida, à direita do limite
    assert serpente.verificar_colisao(20, 20) == True

def test_sem_colisao_dentro_dos_limites():
    """Testa que não há colisão quando a cobra está em uma posição válida."""
    serpente = Snake()
    serpente.posicao = (15, 15) # Posição válida dentro do grid
    assert serpente.verificar_colisao(20, 20) == False

def test_colisao_com_o_proprio_corpo():
    """Testa se a colisão com o próprio corpo é detectada."""
    serpente = Snake()
    # Força um estado em que a cabeça está prestes a colidir com o corpo
    # Corpo: [(10,10), (11,10), (12,10), (11,10)] <- cabeça em (11,10) colide com a cauda
    serpente.corpo = [(10, 10), (11, 10), (12, 10), (11, 10)]
    serpente.posicao = (11, 10) # Posição da cabeça
    
    assert serpente.verificar_colisao(20, 20) == True

def test_sem_colisao_com_o_proprio_corpo():
    """Testa que não há colisão quando o corpo não se cruza."""
    serpente = Snake()
    # Corpo normal, sem cruzamentos
    serpente.corpo = [(10, 10), (9, 10), (8, 10)]
    serpente.posicao = (10, 10)
    
    assert serpente.verificar_colisao(20, 20) == False

