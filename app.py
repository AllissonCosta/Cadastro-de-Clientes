from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone)
            VALUES (?, ?, ?)
        ''', (nome, email, telefone))
        conn.commit()
        conn.close()

    return render_template('index.html', clientes=buscar_clientes())

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return render_template('index.html', clientes=buscar_clientes())


def buscar_clientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

    

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
