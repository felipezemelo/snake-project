# language: pt

Funcionalidade: Controlar a cobra
  Para que eu possa guiar a cobra pela tela, como jogador,
  eu quero usar as setas do teclado para movimentá-la e impedi-la de inverter o curso.

Cenário: Mover a cobra para cima
  # A palavra "direita" agora está entre aspas para ser um parâmetro
  Dado que o jogo começou e a cobra está se movendo para a "direita"
  Quando eu aperto a tecla "seta para cima"
  Então a direção da cobra deve mudar para "cima"

Cenário: Mover a cobra para baixo
  Dado que o jogo começou e a cobra está se movendo para a "direita"
  Quando eu aperto a tecla "seta para baixo"
  Então a direção da cobra deve mudar para "baixo"

Cenário: Impedir que a cobra inverta de direita para esquerda
  Dado que o jogo começou e a cobra está se movendo para a "direita"
  Quando eu aperto a tecla "seta para esquerda"
  Então a direção da cobra deve continuar sendo "direita"

Cenário: Impedir que a cobra inverta de cima para baixo
  Dado que o jogo começou e a cobra está se movendo para a "cima"
  Quando eu aperto a tecla "seta para baixo"
  Então a direção da cobra deve continuar sendo "cima"