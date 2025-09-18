# language: pt

Funcionalidade: Selecionar a dificuldade
  Para que o desafio do jogo se ajuste à minha preferência, como jogador,
  eu quero poder escolher um nível de dificuldade.

Cenário: Selecionar o nível Normal
  Dado que eu estou na tela de seleção de dificuldade
  Quando eu seleciono a opção "Normal"
  Então o jogo deve iniciar no modo Normal

Cenário: Selecionar o nível Difícil
  Dado que eu estou na tela de seleção de dificuldade
  Quando eu seleciono a opção "Difícil"
  Então o jogo deve iniciar no modo Difícil