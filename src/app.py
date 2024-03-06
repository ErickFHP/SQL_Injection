from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask import flash
import sqlite3

from config import config
from conexion_sqlite3 import start_Db

app = Flask(__name__, template_folder='../template')
app.secret_key = 'a_secret'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/begin')
def begin():
    return render_template('begin.html')

#Login
@app.route('/access-login', methods=["GET","POST"])
def login():
    print("Hola1")
    if request.method == 'POST' and 'EmailText' in request.form and 'PassText':
        email = request.form['EmailText']
        password = request.form['PassText']
        print(email, password)
        try:
            conn=sqlite3.connect("db.sqlite3")
            cursor=conn.cursor()
            print("Hola 2")
            sql = "SELECT * FROM users WHERE email = '" + email + "' AND pass = " + password
            print("Hola 3")
            cursor.execute(sql)
            print(sql)
            row=cursor.fetchone()
            cursor.close()
            if row:
                #session['logged'] = True
                #session['id'] = row['id']

                return render_template('begin.html')
            else:
                flash('Datos incorrectos, por favor intenta de nuevo.')
                return render_template('index.html')
        except Exception as ex:
            print(ex)
            return "Error"

@app.route('/users')
def list_users():
    try:
        conn=sqlite3.connect("db.sqlite3")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows=cursor.fetchall()
        cursor.close()
        output = ""
        for row in rows:
            output += f"ID: {row[0]}, Nombre: {row[1]}, Correo: {row[2]}, Contraseña: {row[3]}<br>"
        return output
    except Exception as ex:
        print(ex)
        return "Error"
    
def pagina_404(error):
    return render_template('404Page.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_404)
    start_Db()
    app.run()