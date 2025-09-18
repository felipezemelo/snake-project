# language: pt

Funcionalidade: Visualizar a pontuação final
  Para que eu saiba qual foi meu desempenho na partida, como jogador,
  eu quero ver minha pontuação final em uma tela de "Game Over".

Cenário: Exibição da pontuação final
  Dado que eu terminei uma partida com "150" pontos
  Quando a tela de "Game Over" é exibida
  Então o texto "Pontuação Final: 150" deve estar visível na tela