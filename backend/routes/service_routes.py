from flask import Blueprint, render_template, request, redirect, flash
from utils.auth import verificar_token

service_blueprint = Blueprint("services", __name__)

@service_blueprint.route('/')
def index():
    return render_template('index.html')

@service_blueprint.route('/check')
def check():
    token = request.headers.get('Authorization')
    if not token or not verificar_token(token.split(" ")[1]):
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('check.html')

@service_blueprint.route('/check2')
def check2():
    token = request.headers.get('Authorization')
    if not token or not verificar_token(token.split(" ")[1]):
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('check2.html')

@service_blueprint.route('/servicos')
def servicos():
    token = request.headers.get('Authorization')
    if not token or not verificar_token(token.split(" ")[1]):
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('servicos.html')

@service_blueprint.route('/gerenciador')
def gerenciador():
    token = request.headers.get('Authorization')
    if not token or not verificar_token(token.split(" ")[1]):
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('gerenciador.html')

@service_blueprint.route('/historico')
def historico():
    token = request.headers.get('Authorization')
    if not token or not verificar_token(token.split(" ")[1]):
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('historico.html')