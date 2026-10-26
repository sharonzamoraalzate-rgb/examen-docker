from flask import Flask, request, render_template
import sqlite3, os

DB = os.environ.get("DB_PATH", "/data/productos.db")
app = Flask(__name__)

def get_db():
    return sqlite3.connect(DB)

def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL)""")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = None
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)",
            (request.form["nombre"], request.form["categoria"], request.form["precio"]),
        )
        conn.commit()
        mensaje = "Producto guardado correctamente"
    productos = conn.execute("SELECT id, nombre, categoria, precio FROM productos").fetchall()
    conn.close()
    return render_template("index.html", mensaje=mensaje, productos=productos)

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)