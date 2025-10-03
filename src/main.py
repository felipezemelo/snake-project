# src/main.py
from flask import Flask, render_template, jsonify, request
from src.game import Game

app = Flask(__name__)

# Cria uma instância global do jogo que o servidor irá controlar
game_instance = Game(largura=20, altura=20)

@app.route('/')
def home():
    """Renderiza a página principal do jogo."""
    return render_template('index.html')

# --- ROTAS DE API ---

@app.route('/api/start', methods=['POST'])
def start_game():
    """Inicia um novo jogo, reiniciando a instância no servidor."""
    global game_instance
    game_instance = Game(largura=20, altura=20)
    return jsonify({'message': 'Novo jogo iniciado'})

@app.route('/api/state', methods=['GET'])
def get_state():
    """Retorna o estado atual completo do jogo em formato JSON."""
    global game_instance
    game_instance.update()
    
    state = {
        'snake_body': [segment for segment in game_instance.snake.corpo],
        'food_position': game_instance.board.comida.posicao,
        'score': game_instance.pontuacao,
        'game_over': game_instance.game_over,
        'snake_direction': game_instance.snake.direcao # <-- A linha importante
    }
    return jsonify(state)

@app.route('/api/move', methods=['POST'])
def move_snake():
    """Recebe a nova direção do jogador e a atualiza no jogo."""
    global game_instance
    data = request.get_json()
    direction = data.get('direction')
    
    if direction:
        game_instance.snake.mudar_direcao(direction)
        
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)