# run_game.py
import webbrowser
import threading
from src.main import app

def run_app():
    # Roda a aplicação Flask. Desativamos o modo de depuração para a versão final.
    app.run(debug=False)

if __name__ == '__main__':
    # Inicia o servidor Flask numa thread separada para não bloquear o resto do script
    server_thread = threading.Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()

    # Abre o navegador na página do jogo
    webbrowser.open("http://127.0.0.1:5000/")

    # O script principal pode terminar aqui, mas a thread do servidor continuará a rodar
    # (Podemos adicionar uma lógica de espera se necessário, mas para este caso é suficiente)
    input("O servidor do jogo está a rodar. Pressione Enter para fechar...\n")