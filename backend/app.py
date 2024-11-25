import os
import pymysql
import jwt
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor
}

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

def get_db_connection():
    """
    Função para conectar ao banco de dados
    """
    return pymysql.connect(**db_config)

def generate_jwt_token(user):
    """
    Função para gerar o token JWT para o usuário
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
    payload = {
        'user_id': user['id'],  
        'email': user['email'],  
        'exp': expiration  
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') 
    return token

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Endpoint para o cadastro de novos usuários.
    """
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Endpoint de login que verifica as credenciais do usuário e retorna o JWT se o login for bem-sucedido.
    """
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                    user = cursor.fetchone()

                    if user and check_password_hash(user['senha'], senha):

                        token = generate_jwt_token(user)

                        return redirect(url_for('servicos', token=token))  # Redireciona para a página de serviços
                    else:
                        return jsonify({"msg": "Credenciais inválidas"}), 401
        except Exception as e:
            return jsonify({"msg": f"Erro ao fazer login: {e}"}), 500

    return render_template('login.html')

@app.route('/servicos', methods=['GET', 'POST'])
def servicos():
    """
    Endpoint para mostrar os serviços disponíveis.
    """
    if request.method == 'POST':

        pass

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM servicos WHERE status = 'ativo'")
                servicos = cursor.fetchall()
        return render_template('servicos.html', servicos=servicos)
    except Exception as e:
        return jsonify({"msg": f"Erro ao listar serviços: {e}"}), 500

@app.route('/historico', methods=['GET', 'POST'])
def historico():
    """
    Endpoint para mostrar o histórico de serviços de um usuário.
    """
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        servico_id = request.form['servico_id']

        pass
    
    usuario_id = request.args.get('usuario_id') 
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM historico WHERE usuario_id = %s", (usuario_id,))
                historico = cursor.fetchall()
        return render_template('historico.html', historico=historico)
    except Exception as e:
        return jsonify({"msg": f"Erro ao obter histórico: {e}"}), 500

@app.route('/gerenciador', methods=['GET', 'POST'])
def gerenciador():
    """
    Endpoint para gerenciamento de serviços e usuários.
    """
    if request.method == 'POST':
        servico_id = request.form['servico_id']
        novo_status = request.form['status']
        
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE servicos SET status = %s WHERE id = %s", (novo_status, servico_id))
                    conn.commit()
        except Exception as e:
            return jsonify({"msg": f"Erro ao atualizar serviço: {e}"}), 500

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios")
                usuarios = cursor.fetchall()
                cursor.execute("SELECT * FROM servicos")
                servicos = cursor.fetchall()

        return render_template('gerenciador.html', usuarios=usuarios, servicos=servicos)
    except Exception as e:
        return jsonify({"msg": f"Erro ao acessar gerenciador: {e}"}), 500

@app.route('/check', methods=['GET', 'POST'])
def check():
    """
    Endpoint para o check-in dos usuários nos serviços.
    """
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        servico_id = request.form['servico_id']

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO checkins (usuario_id, servico_id) VALUES (%s, %s)", (usuario_id, servico_id))
                    conn.commit()
            return redirect(url_for('historico', usuario_id=usuario_id)) 
        except Exception as e:
            return jsonify({"msg": f"Erro ao realizar check-in: {e}"}), 500

    return render_template('check.html')

@app.route('/')
def index():
    """
    Página inicial.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)