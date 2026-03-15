import sqlite3
import hashlib

DB = "usuarios.db"

# Crear tabla si no existe
def crear_tabla():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

# Función para agregar usuario
def agregar_usuario(nombre, password):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Verificar si hay algún usuario en la tabla
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad = cursor.fetchone()[0]

    # Primer usuario → contraseña en texto plano
    if cantidad == 0:
        pwd_guardada = password
        print("Primer usuario, contraseña sin cifrar.")
    else:
        # Otros usuarios → cifrar con SHA-256
        pwd_guardada = hashlib.sha256(password.encode()).hexdigest()
        print("Usuario nuevo, contraseña cifrada con SHA-256.")

    try:
        cursor.execute("INSERT INTO usuarios(nombre, password) VALUES (?, ?)", (nombre, pwd_guardada))
        conn.commit()
        print(f"Usuario '{nombre}' agregado correctamente.")
    except sqlite3.IntegrityError:
        print(f"Error: El usuario '{nombre}' ya existe.")
    conn.close()


if __name__ == "__main__":
    crear_tabla()

    while True:
        print("\n--- Registrar Usuario ---")
        nombre = input("Nombre: ")
        password = input("Password: ")

        agregar_usuario(nombre, password)

        continuar = input("¿Agregar otro usuario? (s/n): ").lower()
        if continuar != "s":
            break