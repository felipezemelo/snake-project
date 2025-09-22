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


