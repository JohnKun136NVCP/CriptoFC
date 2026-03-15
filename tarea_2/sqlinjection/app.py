from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    productos = [
        {"nombre":"Figura Hatsune Miku 15to Aniversario","precio":4867.11,"img":"https://www.goodsmile.com/gsc-webrevo-sdk-storage-prd/product/image/product/20220829/13164/103381/large/6aea3626b0df598311da93f9f975813b.jpg"},
        {"nombre":"Project VOLTAGE 18 Types / Songs Collection (Original Soundtrack)","precio":1278.98,"img":"https://m.media-amazon.com/images/I/71Kq-hYT7ZL._AC_SX679_.jpg"},
        {"nombre":"Póster impreso de Miku Day (Vocaloid) de 8,5 x 11 pulgadas","precio":281.12,"img":"https://i.etsystatic.com/10288422/r/il/b12690/3046060604/il_1588xN.3046060604_8be7.jpg"},
        {"nombre":"Teclado gamer retroiluminado español con interruptor optomecánico TUF gaming K3 gen II Hatsune Miku edition","precio":150,"img":"https://ss637.liverpool.com.mx/xl/1184690574.jpg"},
        {"nombre":"Figura Megurine Luka","precio":329.57,"img":"https://www.goodsmile.com/gsc-webrevo-sdk-storage-prd/product/image/product/20100628/2896/10552/large/e96850e6af3bc94af4302b8e88d3e5c0.jpg"},
        {"nombre":"GSR Character Customize Series: Hatsune Miku 1/24 Scale Decals 01","precio":247.12,"img":"https://www.goodsmile.com/gsc-webrevo-sdk-storage-prd/product/image/product/20091023/2221/6109/large/c70d9b4410230c09278483760f3b0d26.jpg"},
    ]
    return render_template("index.html", productos=productos)

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    print("LOGIN:", usuario, password)

    conn = get_db()
    cursor = conn.cursor()

    # SQL vulnerable intencional
    query = f"SELECT * FROM usuarios WHERE nombre='{usuario}' AND password='{password}'"
    cursor.execute(query)
    resultados = cursor.fetchall()

    if resultados:
        conn.close()
        # simulamos login: devolvemos redirect
        return jsonify({"success": True, "redirect": "/admin"})

    # Probar con SHA256
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query_hash = f"SELECT * FROM usuarios WHERE nombre='{usuario}' AND password='{password_hash}'"
    cursor.execute(query_hash)
    resultados_hash = cursor.fetchall()
    conn.close()

    if resultados_hash:
        return jsonify({"success": True, "redirect": "/admin"})
    else:
        return jsonify({"success": False, "message": "Login incorrecto"})


@app.route("/admin")
def admin_page():
    # No usamos session: solo simulamos que el login fue correcto
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()
    conn.close()

    imagenes = [
        "https://tryhackme-images.s3.amazonaws.com/room-icons/7a8797ae59733f2a72f0e8a8748be128.jpeg?img=1",
        "https://piapro.net/intl/images/btn_miku.jpg?img=2",
        "https://piapro.net/intl/images/btn_rin.jpg?img=3",
        "https://piapro.net/intl/images/btn_len.jpg?img=4",
        "https://i.pravatar.cc/150?img=5",
        "https://i.pravatar.cc/150?img=6",
        "https://piapro.net/intl/images/btn_kaitov3.jpg?img=7",
        "https://piapro.net/intl/images/btn_luka.jpg?img=8",
        "https://piapro.net/intl/images/btn_meikov3.jpg?img=9",
        "https://static.wikia.nocookie.net/synthv/images/4/44/GUMI_AI_My_Dreamtonics_Icon.png?img=10"
        
    ]

    usuarios_lista = []
    for i, fila in enumerate(resultados):
        img = imagenes[i % len(imagenes)]
        usuarios_lista.append({
            "nombre": fila["nombre"],
            "password": fila["password"],
            "img": img
        })

    return render_template("admin.html", usuarios=usuarios_lista)


@app.route("/logout")
def logout():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)