from flask import Blueprint, render_template, request, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
from utils.auth import gerar_token
from utils.validators import validar_email
from contextlib import closing
import pymysql

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if not validar_email(email):
            flash("Email inválido!", "error")
            return redirect("/login")

        with closing(get_db_connection()) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user[3], senha):
            token = gerar_token(user[0])
            return jsonify({"token": token}), 200
        else:
            flash("Login falhou! Verifique seu email e senha.", "error")
            return redirect("/login")
        
    return render_template("login.html")

@auth_blueprint.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if not validar_email(email):
            flash("Email inválido!", "error")
            return redirect("/cadastro")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return redirect("/cadastro")

        with closing(get_db_connection()) as db:
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email já cadastrado!", "error")
                return redirect("/cadastro")

            hashed_password = generate_password_hash(senha)

            try:
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, hashed_password))
                db.commit()
                flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
            except pymysql.Error as e:
                flash(f"Erro ao cadastrar usuário: {e}", "error")
                return redirect("/cadastro")
    
        return redirect("/login")
    
    return render_template("cadastro.html")

@auth_blueprint.route('/logout')
def logout():
    flash("Você foi desconectado com sucesso.", "sucesso")
    return redirect("/login")