# 🐍 Jogo Snake com BDD e TDD

Este projeto é o desenvolvimento de um jogo **Snake clássico** com uma interface web, criado como parte da disciplina de **Teste de Software**.  
O principal objetivo é aplicar os princípios de **Teste Holístico**, utilizando **BDD (Behavior Driven Development)** e **TDD (Test Driven Development)** para guiar a construção do software.

---

## 📌 Status do Projeto / TO-DO

- [x] **Fase 1:** Discovery e Brainstorming de ideias  
- [x] **Fase 2:** Planejamento e Definição do MVP com Histórias de Usuário  
- [x] **Fase 3:** Criação de todos os Cenários de Teste BDD (`.feature`)  
- [x] **Fase 4:** Configuração do Ambiente Python e da estrutura do projeto  
- [x] **Fase 5:** Implementação dos primeiros *Step Definitions* (`partida_steps.py`, `dificuldade_steps.py`)  
- [x] **Fase 5.1:** Implementar os 4 *Step Definitions* restantes  
- [x] **Fase 6:** Desenvolvimento da Lógica do Jogo (`snake.py` e `game.js`) com TDD  
- [x] **Fase 7:** Realizar Testes Informais com usuários e registrar *Issues*  
- [ ] **Fase 8:** Escrever o Relatório Técnico Final  

---

## 🛠 Tecnologias Utilizadas

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Testes BDD:** Behave, Selenium  
- **Testes TDD:** Pytest  

---

## ⚙️ Configuração do Ambiente

### 1. Criar e Ativar o Ambiente Virtual

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell)
.\.venv\Scripts\activate

# Ativar no Linux/Mac
source .venv/bin/activate
```
### 2. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 🚀 Como Executar

```bash
# 1. Rodar a Aplicação Web:
python src/main.py

# 2. Rodar os Testes BDD:
behave

TO-DO
# 3. Rodar os Testes TDD (Unitários) 
pytest
