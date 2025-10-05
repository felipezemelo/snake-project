# src/main.py
from flask import Flask, render_template, jsonify, request
from src.game import Game

app = Flask(__name__)
game_instance = Game(largura=20, altura=20)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_game():
    global game_instance
    game_instance = Game(largura=20, altura=20)
    return jsonify({'message': 'Novo jogo iniciado'})

@app.route('/api/state', methods=['GET'])
def get_state():
    global game_instance
    game_instance.update()
    state = {
        'snake_body': [segment for segment in game_instance.snake.corpo],
        'food': { 'position': game_instance.board.comida.posicao, 'type': game_instance.board.comida.type },
        'score': game_instance.pontuacao,
        'game_over': game_instance.game_over,
        'snake_direction': game_instance.snake.direcao
    }
    return jsonify(state)

@app.route('/api/move', methods=['POST'])
def move_snake():
    global game_instance
    data = request.get_json()
    direction = data.get('direction')
    if direction:
        game_instance.snake.mudar_direcao(direction)
    return jsonify({'status': 'success'})

@app.route('/api/test/set_snake', methods=['POST'])
def set_snake_for_testing():
    """Define o corpo e a direção da cobra para um teste."""
    global game_instance
    data = request.get_json()
    
    body = data.get('body')
    direction = data.get('direction')
    
    if body:
        # Converte a lista de listas para uma lista de tuplos
        game_instance.snake.corpo = [tuple(segment) for segment in body]
        game_instance.snake.posicao = game_instance.snake.corpo[0]
        game_instance.snake.tamanho = len(body)
        
    if direction:
        game_instance.snake.direcao = direction.upper()
        
    return jsonify({'status': 'success'})



@app.route('/api/get_current_state', methods=['GET'])
def get_current_state():
    """Retorna o estado atual do jogo sem o modificar."""
    global game_instance
    state = {
        'snake_body': [segment for segment in game_instance.snake.corpo],
        'food': { 'position': game_instance.board.comida.posicao, 'type': game_instance.board.comida.type } if game_instance.board.comida else None,
        'score': game_instance.pontuacao,
        'game_over': game_instance.game_over,
        'snake_direction': game_instance.snake.direcao
    }
    return jsonify(state)

if __name__ == '__main__':
    app.run(debug=True)