# language: pt
Funcionalidade: Controlar a cobra
  Para que eu possa guiar a cobra pela tela, como jogador,
  eu quero usar as setas do teclado para movimentá-la.

Cenário: Mover a cobra para cima
  Dado que o jogo começou e a cobra está se movendo para a direita
  Quando eu aperto a tecla "seta para cima"
  Então a direção da cobra deve mudar para "cima"