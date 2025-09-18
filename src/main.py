# Importa a classe Flask e a função render_template
from flask import Flask, render_template

# Cria uma instância da aplicação web
# O argumento __name__ ajuda o Flask a encontrar a pasta 'templates'
app = Flask(__name__)

# Define a rota para a página inicial do site ('/')
@app.route('/')
def home():
    """Esta função será executada quando alguém acessar a página inicial."""
    # Retorna o conteúdo do arquivo index.html que está na pasta 'templates'
    return render_template('index.html')

# Este bloco garante que o servidor só vai rodar quando o script for executado diretamente
if __name__ == '__main__':
    # Roda a aplicação em modo de depuração, que reinicia automaticamente a cada mudança
    app.run(debug=True)