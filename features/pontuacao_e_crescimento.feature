# language: pt

Funcionalidade: Aumentar a pontuação e o tamanho
  Para que eu tenha um retorno sobre meu progresso no jogo, como jogador,
  eu quero que a cobra cresça e a pontuação aumente ao comer um "Rato Cinza".

Cenário: Cobra come um Rato Cinza
  Dado que eu estou em uma partida com pontuação "50" e a cobra tem tamanho "10"
  E um "Rato Cinza" está na célula à frente da cobra
  Quando a cobra se move e come o "Rato Cinza"
  Então minha pontuação deve ser "55"
  E o tamanho da cobra deve ser "11"