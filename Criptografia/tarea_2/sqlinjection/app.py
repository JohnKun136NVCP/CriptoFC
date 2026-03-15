from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login_inseguro():
    data = request.get_json()  
    usuario = data.get("usuario")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM usuarios WHERE nombre='{usuario}' AND password='{password}'"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()

    salida = "<h2>Users??</h2><ul>"
    for fila in resultados:
        salida += f"<li>{fila['nombre']} - {fila['password']}</li>"
    salida += "</ul>"
    return salida


if __name__ == "__main__":
    app.run(debug=True)
