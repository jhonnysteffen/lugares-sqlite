from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = "lugares.db"

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE lugares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            comida TEXT NOT NULL,
            essencial TEXT NOT NULL,
            visitado INTEGER DEFAULT 0
        )
        """)
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome")
        comida = request.form.get("comida")
        essencial = request.form.get("essencial")
        cursor.execute("INSERT INTO lugares (nome, comida, essencial) VALUES (?, ?, ?)", (nome, comida, essencial))
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT id, nome, comida, essencial, visitado FROM lugares")
    lugares = cursor.fetchall()
    conn.close()
    return render_template("index.html", lugares=lugares)

@app.route("/visitar/<int:lugar_id>")
def visitar(lugar_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE lugares SET visitado = 1 WHERE id = ?", (lugar_id,))
    conn.commit()
    conn.close()
    return redirect("/")

init_db()

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/desmarcar/<int:lugar_id>")
def desmarcar(lugar_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE lugares SET visitado = 0 WHERE id = ?", (lugar_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/deletar/<int:lugar_id>")
def deletar(lugar_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lugares WHERE id = ?", (lugar_id,))
    conn.commit()
    conn.close()
    return redirect("/")

