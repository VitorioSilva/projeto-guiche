import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="../frontend/templates",
                      static_folder="../frontend/static")

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

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

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user and check_password_hash(user['senha'], senha):
                    access_token = create_access_token(identity={'id': user['id'], 'permissao': user['permissao']})
                    return jsonify(access_token=access_token)
                else:
                    return jsonify({"msg": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"msg": f"Erro ao fazer login: {e}"}), 500

@app.route('/servicos', methods=['GET'])
def servicos():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM servicos WHERE status = 'ativo'")
                servicos = cursor.fetchall()
        return render_template('servicos.html', servicos=servicos)
    except Exception as e:
        return jsonify({"msg": f"Erro ao listar serviços: {e}"}), 500

@app.route('/historico', methods=['GET'])
@jwt_required()
def historico():
    current_user = get_jwt_identity()
    usuario_id = current_user['id']
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM historico WHERE usuario_id = %s", (usuario_id,))
                historico = cursor.fetchall()
        return render_template('historico.html', historico=historico)
    except Exception as e:
        return jsonify({"msg": f"Erro ao obter histórico: {e}"}), 500

@app.route('/gerenciador', methods=['GET', 'POST'])
@jwt_required()
def gerenciador():
    current_user = get_jwt_identity()
    if current_user['permissao'] != 'admin':
        return jsonify({"msg": "Acesso negado"}), 403

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

@app.route('/check', methods=['POST'])
@jwt_required()
def check():
    usuario_id = request.form['usuario_id']
    servico_id = request.form['servico_id']

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO checkins (usuario_id, servico_id) VALUES (%s, %s)", (usuario_id, servico_id))
                conn.commit()
        return redirect(url_for('historico'))
    except Exception as e:
        return jsonify({"msg": f"Erro ao realizar check-in: {e}"}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)