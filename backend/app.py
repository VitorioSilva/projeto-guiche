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
    return render_template("servicos.html")

@app.route("/gerenciador")
def gerenciador():
    return render_template("gerenciador.html")

@app.route("/historico")
def historico():
    return render_template("historico.html")

@app.route("/check")
def check():
    return render_template("check.html")

if __name__ == "__main__":
    app.run(debug=True)