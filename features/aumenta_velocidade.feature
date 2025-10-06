# language: pt

Funcionalidade: Aumentar a dificuldade com a pontuação
  Para que o jogo se torne mais desafiador conforme eu progrido, como jogador,
  eu quero que a velocidade da cobra aumente em determinados marcos de pontuação no modo Normal.

Cenário: Velocidade aumenta ao atingir o primeiro marco de pontuação
  Dado que eu estou em uma partida no modo "Normal" com a velocidade inicial
  E minha pontuação é "45"
  Quando a cobra come um "Rato Normal" e minha pontuação se torna "50"
  Então a velocidade do jogo deve aumentar para o "nível 2"

Cenário: Velocidade aumenta novamente ao atingir o segundo marco
  Dado que eu estou em uma partida no modo "Normal" com a velocidade no "nível 2"
  E minha pontuação é "95"
  Quando a cobra come um "Rato Normal" e minha pontuação se torna "100"
  Então a velocidade do jogo deve aumentar para o "nível 3"

Cenário: A velocidade não deve aumentar se o marco de pontuação não for atingido
  Dado que eu estou em uma partida no modo "Normal" com a velocidade inicial
  E minha pontuação é "30"
  Quando a cobra come um "Rato Normal" e minha pontuação se torna "35"
  Então a velocidade do jogo deve permanecer a mesma

Cenário: A velocidade não deve aumentar no modo Difícil
  Dado que eu estou em uma partida no modo "Difícil" com a velocidade inicial
  E minha pontuação é "45"
  Quando a cobra come um "Rato Normal" e minha pontuação se torna "50"
  Então a velocidade do jogo deve permanecer a mesma