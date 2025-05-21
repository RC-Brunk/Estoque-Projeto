import os
from flask import Flask, request, jsonify, render_template
#Causa do CORS: O Live Server do VSCode (usado para abrir index.html) usa a porta 5500 por padrão, enquanto o Flask usa a porta 5000. Isso cria uma origem diferente, exigindo o cabeçalho CORS. 
from flask_cors import CORS
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)


def init_db():
    conn = None
    try:
        conn = sqlite3.connect('database.db', timeout=10)
        conn.execute('PRAGMA busy_timeout = 10000')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar o banco: {str(e)}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco fechada")

# Rota inicial para renderizar o frontend
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint GET /produtos - Listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = None
    try:
        conn = sqlite3.connect('database.db', timeout=10)
        conn.execute('PRAGMA busy_timeout = 10000')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        return jsonify([{'id': p[0], 'nome': p[1], 'quantidade': p[2], 'categoria': p[3]} for p in produtos])
    except Exception as e:
        print(f"Erro no backend: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco fechada")

# Endpoint POST /produtos - Adicionar um produto
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    conn = None  # Inicializar como None para garantir que será fechado
    try:
        data = request.get_json(force=True)
        print("Dados recebidos:", data)
        if not data or 'nome' not in data or 'quantidade' not in data or 'categoria' not in data:
            print("Erro: Dados incompletos ou inválidos")
            return jsonify({'error': 'Dados incompletos ou inválidos'}), 400
        nome = data['nome']
        quantidade = data['quantidade']
        categoria = data['categoria']
        print("Valores extraídos:", nome, quantidade, categoria)

        conn = sqlite3.connect('database.db', timeout=10)  # Adicionar timeout
        conn.execute('PRAGMA busy_timeout = 10000')  # Adicionar para lidar com bloqueios
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produtos (nome, quantidade, categoria) VALUES (?, ?, ?)',
                       (nome, quantidade, categoria))
        conn.commit()
        print("Produto inserido com sucesso")
        return jsonify({'message': 'Produto adicionado!'}), 201
    except Exception as e:
        print(f"Erro no backend: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco fechada")  # Adicionar para depuração
    
# Endpoint PUT /produtos/<id> - Atualizar um produto
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    conn = None
    try:
        data = request.get_json(force=True)
        print("Dados recebidos:", data)
        if not data or 'nome' not in data or 'quantidade' not in data or 'categoria' not in data:
            print("Erro: Dados incompletos ou inválidos")
            return jsonify({'error': 'Dados incompletos ou inválidos'}), 400
        nome = data['nome']
        quantidade = data['quantidade']
        categoria = data['categoria']
        print("Valores extraídos:", nome, quantidade, categoria)

        conn = sqlite3.connect('database.db', timeout=10)
        conn.execute('PRAGMA busy_timeout = 10000')
        cursor = conn.cursor()
        cursor.execute('UPDATE produtos SET nome = ?, quantidade = ?, categoria = ? WHERE id = ?',
                       (nome, quantidade, categoria, id))
        conn.commit()
        print("Produto atualizado com sucesso")
        return jsonify({'message': 'Produto atualizado!'}), 200
    except Exception as e:
        print(f"Erro no backend: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco fechada")

# Endpoint DELETE /produtos/<id> - Excluir um produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    conn = None
    try:
        conn = sqlite3.connect('database.db', timeout=10)
        conn.execute('PRAGMA busy_timeout = 10000')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conn.commit()
        print("Produto excluído com sucesso")
        return jsonify({'message': 'Produto excluído!'}), 200
    except Exception as e:
        print(f"Erro no backend: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco fechada")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)