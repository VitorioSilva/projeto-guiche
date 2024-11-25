import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configurações do app Flask
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "sua_chave_secreta_segura")

# Configurações do banco de dados
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor
}

# Função para conectar ao banco de dados
def get_db_connection():
    return pymysql.connect(**db_config)

# Decorator para proteger rotas com JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Token esperado no cabeçalho
        if not token:
            return jsonify({'msg': 'Token de autenticação é necessário!'}), 403

        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = decoded['user_id']  # Adiciona user_id ao request
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Token inválido!'}), 401

        return f(*args, **kwargs)
    return decorated

# Endpoint de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
                    conn.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return jsonify({"msg": f"Erro ao cadastrar usuário: {e}"}), 500

    return render_template('cadastro.html')

# Endpoint de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                    user = cursor.fetchone()
                    if user and check_password_hash(user['senha'], senha):
                        # Gerar um token JWT
                        token = jwt.encode({
                            'user_id': user['id'],
                            'exp': datetime.utcnow() + timedelta(hours=1)
                        }, app.config['SECRET_KEY'], algorithm='HS256')

                        return jsonify({'token': token}), 200
                    else:
                        return jsonify({"msg": "Credenciais inválidas"}), 401
        except Exception as e:
            return jsonify({"msg": f"Erro ao fazer login: {e}"}), 500

    return render_template('login.html')

# Endpoint protegido: serviços
@app.route('/servicos', methods=['GET', 'POST'])
@token_required
def servicos():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM servicos WHERE status = 'ativo'")
                servicos = cursor.fetchall()
        return render_template('servicos.html', servicos=servicos)
    except Exception as e:
        return jsonify({"msg": f"Erro ao listar serviços: {e}"}), 500

# Endpoint protegido: histórico
@app.route('/historico', methods=['GET'])
@token_required
def historico():
    usuario_id = request.user_id
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM historico WHERE usuario_id = %s", (usuario_id,))
                historico = cursor.fetchall()
        return render_template('historico.html', historico=historico)
    except Exception as e:
        return jsonify({"msg": f"Erro ao obter histórico: {e}"}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)