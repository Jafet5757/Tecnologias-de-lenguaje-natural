from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "¡Hola, mundo!"

@app.route("/saludo/<nombre>", methods=["GET"])
def saludo(nombre):
    return f"Hola, {nombre}!"

@app.route("/render")
def render():
    nombre = request.args.get("name")
    return render_template("index.html", name=nombre)