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
    if request.method == 'POST' and 'EmailText' in request.form and 'PassText':
        email = request.form['EmailText']
        password = request.form['PassText']
        print(email, password)
        try:
            conn=sqlite3.connect("db.sqlite3")
            cursor=conn.cursor()
            sql = "SELECT * FROM users WHERE email = '" + email + "' AND pass = " + password
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

@app.route('/products')
def list_products():
    try:
        conn=sqlite3.connect("db.sqlite3")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows=cursor.fetchall()
        cursor.close()
        output = ""
        for row in rows:
            output += f"ID: {row[0]}, Product: {row[1]}, Price: {row[2]}<br>"
        return output
    except Exception as ex:
        print(ex)
        return "Error"

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/insertForm')
def insertForm():
    return render_template('insertForm.html')

@app.route('/insert-product', methods=('GET', 'POST'))
def insert_product():
    if request.method == 'POST' and 'product_name' in request.form and 'unit_price':
        try:
            conn=sqlite3.connect("db.sqlite3")
            cursor=conn.cursor()

            product_name = request.form['product_name']
            unit_price = request.form['unit_price']
            sql = "INSERT INTO products (product, price) VALUES ('" + product_name + "', " + unit_price + ")"
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()
            flash('Producto introducido con éxito!', 'success')
        except Exception as ex:
            print(ex)
            flash('Hubo un problema', 'error')

    return render_template('insertForm.html')

@app.route('/searchProducts')
def searchProducts():
    return render_template('searchProducts.html')

@app.route('/search-product', methods=('GET', 'POST'))
def search_product():
    products = []
    if request.method == 'POST':
        product_name = request.form['product_name']

        conn=sqlite3.connect("db.sqlite3")
        cursor=conn.cursor()
        sql = "SELECT * FROM products WHERE product like '%" + product_name + "%'"
        print(sql)
        cursor.execute(sql)
        products = cursor.fetchall()
        print(products)
        conn.close()
        return render_template('searchProducts.html', products=products)

    return render_template('searchProducts.html')

def pagina_404(error):
    return render_template('404Page.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_404)
    start_Db()
    app.run()