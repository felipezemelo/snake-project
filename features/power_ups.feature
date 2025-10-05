# language: pt

Funcionalidade: Efeitos dos Ratos Especiais
  Para tornar o jogo mais dinâmico e desafiador, como jogador,
  eu quero que ratos de cores diferentes concedam bônus ou penalidades.

Cenário: Cobra come um Rato Dourado e ganha um grande bônus de pontos
  Dado que eu estou em uma partida com pontuação "100" e a cobra tem tamanho "10"
  E um "Rato Dourado" está na célula à frente da cobra
  Quando a cobra se move e come o "Rato Dourado"
  Então minha pontuação deve ser "125"
  E o tamanho da cobra deve ser "11"

Cenário: Cobra come um Rato Vermelho e encolhe
  Dado que eu estou em uma partida com pontuação "200" e a cobra tem tamanho "12"
  E um "Rato Vermelho" está na célula à frente da cobra
  Quando a cobra se move e come o "Rato Vermelho"
  Então minha pontuação deve ser "201"
  E o tamanho da cobra deve ser "6"