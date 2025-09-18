# language: pt

Funcionalidade: Encerrar o jogo por colisão
  Para que exista uma condição clara de derrota, como jogador,
  eu quero que a partida termine se a cobra colidir com a parede ou com ela mesma.

Cenário: Colisão com a parede superior
  Dado que a cobra está na borda superior do cenário e se movendo para "cima"
  Quando a cobra tenta se mover mais uma vez
  Então a tela de "Game Over" deve ser exibida

Cenário: Colisão com o próprio corpo
  Dado que a cobra tem tamanho "10" e está prestes a cruzar seu próprio corpo
  Quando a cobra se move
  Então a tela de "Game Over" deve ser exibida