from flask import Flask, redirect, render_template

app = Flask(__name__, template_folder="../frontend/templates",
                      static_folder="../frontend/static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/servicos")
def servicos():
    return render_template("/servicos.html")

@app.route("/gerenciador")
def gerenciador():
    return render_template("gerenciador.html")