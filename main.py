from flask import Flask, redirect, render_template, request, url_for
import pyodbc

#Instanciacion del modulo Flask
app = Flask(__name__)

#Datos para la conexion con SQL Server
servidor="192.168.0.97"
base="Global"
usuario="globalsql"
contraseña="010101zxAS"

#Esta funcion permite conectar a la base de datos SQL Server y retorna un curso
def conectar_base():
    conexion = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL server;SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(servidor,base,usuario,contraseña))
    cursor = conexion.cursor()
    return cursor

#Redireccion al login 
@app.route('/')
def Login():
    return render_template('login.html')

#Redireccion a la pagina de busqueda y consulta de datos
@app.route('/view')
def Buscador():
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web')
    data = cur.fetchall()
    for dato in data:
        dato[1]=int(dato[1])
        dato[2]=int(dato[2])
    return render_template('buscador.html', valores = data)

#Logica del login, redirecciona al login si hay error y da acceso al buscador si se registra bien
@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = conectar_base()
        cur.execute('SELECT * FROM web_user_inventory WHERE USUARIO=\''+usuario+'\' AND CONTRASEÑA=\''+contraseña+'\';')
        data = cur.fetchall()
        if data is None :
            return redirect(url_for('Login'))
        else:
            return redirect(url_for('Buscador'))

#Redirecciona a la pagina de detalles 
@app.route('/detalle/<string:id>')
def Mostrar_detalle(id):
    cur = conectar_base()
    cur.execute('SELECT * FROM inve_web where CODIGO = \''+id+'\';')
    data = cur.fetchall()
    return render_template('detalle.html',detalles=data[0])

@app.route('/view/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        codigo = request.form['codigo']
        cur = conectar_base()
        cur.execute('SELECT * FROM inve_web WHERE CODIGO=\''+codigo+'\';')
        data = cur.fetchall()
        for dato in data:
            dato[1]=int(dato[1])
            dato[2]=int(dato[2])
        return render_template('buscador.html', valores = data)
        


if __name__ == '__main__' :
    app.run(port=3000,debug=True)