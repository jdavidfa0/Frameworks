from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import tempfile

app = Flask(__name__)
app.secret_key ='21061976'



db = mysql.connector.connect(
    host="localhost", user="root", password="", database="agenda"
)

cursor = db.cursor()

@app.route('/password/<contraencip>')
def encriptarcontra(contraencrip):
    encriptar=generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)

   # return "Encriptado:{0} | coincide:{1}".format(encriptar,valor)
    return valor


@app.route("/")
def lista():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM personas")
    usuario = cursor.fetchall()
    return render_template("index.html", personas=usuario)

@app.route("/Lista_canciones", methods=["GET", "POST"])
def lista_cancion():
    cursor= db.cursor()
    cursor.execute("SELECT * FROM canciones")
    cancion = cursor.fetchall()
    return render_template("Lista_canciones.html", canciones=cancion)
   
  


@app.route('/verificar')
def usuario_existe():
    return render_template('verificar.html')
    

@app.route("/registrar", methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":
        nombre = request.form.get("Nombreper")
        apellido = request.form.get("apellidoper")
        correo = request.form.get("emailper")
        direccion = request.form.get("dirreccionper")
        telefono = request.form.get("telefonoper")
        usuario = request.form.get("usuarioper")
        contrasena = request.form.get("contraper")
        
        contrasenaencriptada=generate_password_hash(contrasena)

        cursor.execute('SELECT * FROM personas WHERE usuarioper=%s',(usuario,))
        resultado1=cursor.fetchall()
        cursor.execute('SELECT * FROM personas WHERE emailper=%s',(correo,))
        resultado2=cursor.fetchall()
        
    
        if len(resultado1)>0 or len(resultado2)>0:
            print("Usuario o correo ya existe")
            return redirect(url_for('usuario_existe'))
        else:
    # insertar datos a la tabla persona
            cursor.execute(
                "insert into personas( Nombreper ,apellidoper ,emailper ,dirreccionper ,telefonoper ,usuarioper ,contraper )values(%s,%s,%s,%s,%s,%s,%s)",
                (nombre, apellido, correo, direccion, telefono, usuario, contrasenaencriptada),
            )
            db.commit()
            #flash("usuario creado correctamente", "sucess")

            return redirect(url_for("login"))

    return render_template("Registrar.html")



@app.route("/editar/<int:id>", methods=["POST", "GET"])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == "POST":
        nombreper = request.form.get("nombre")
        apelldioper = request.form.get("apellido")
        emailper = request.form.get("email")
        dirreccionper = request.form.get("direccion")
        telefonoper = request.form.get("telefono")
        usuarioper = request.form.get("usuario")
        contraper = request.form.get("contra")

        sql = "update personas set Nombreper=%s, apellidoper=%s,emailper=%s,dirreccionper=%s, telefonoper=%s,usuarioper=%s, contraper=%s where idpersona=%s"
        cursor.execute(
            sql,
            (
                nombreper,
                apelldioper,
                emailper,
                dirreccionper,
                telefonoper,
                usuarioper,
                contraper,
                id,
            ),
        )
        db.commit()

        return redirect(url_for("lista"))

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas WHERE idpersona=%s", (id,))
        data = cursor.fetchall()
        return render_template("editar.html", usuario=data[0])


@app.route("/eliminar/<int:id>", methods=["GET"])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM personas WHERE idpersona=%s',(id,))
       db.commit()
       return redirect(url_for("lista"))
    
@app.route("/login", methods=['GET','POST'] )
def login():
    if request.method == 'POST':
        username=request.form.get('usuarioinir')
        password= request.form.get('contraini')

        cursor=db.cursor()
        cursor.execute("SELECT usuarioper, contraper from personas WHERE usuarioper=%s", (username,))
        resultado=cursor.fetchone()

       
        if resultado and check_password_hash(resultado[1],password):
            session['usuario']=username
            
            return redirect(url_for('lista'))
        else:
            error='Credenciales invalidas, intente denuevo'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('usuario', None)
    print("La sesión se cerró")
    return redirect(url_for('login'))


@app.route("/regis_canciones", methods=["GET", "POST"])
def registrar_cancion():
    if request.method == "POST":
        titulo = request.form.get("titulocan")
        artista = request.form.get("artistacan")
        genero = request.form.get("generocan")
        precio = request.form.get("preciocan")
        duracion= request.form.get("duracioncan")
        lanzamiento = request.form.get("fechacan")
        imagen= request.form.get("imagencan")
        
        cursor.execute("insert into canciones( titulo,artista ,genero,precio,duracion ,lanzamiento ,img)values(%s,%s,%s,%s,%s,%s,%s)",
        (titulo, artista, genero, precio, duracion,lanzamiento, imagen),)
        db.commit()

        return redirect(url_for("registrar_cancion"))

    return render_template("regis_canciones.html")

@app.route("/eliminar_cancion/<int:id>", methods=["GET"])
def eliminar_cancion(id):

    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM canciones WHERE id_can=%s',(id,))
       db.commit()
       return redirect(url_for("lista_cancion"))
    

@app.route("/actu_canciones/<int:id>", methods=["POST", "GET"])
def actualizar_canciones(id):
    cursor = db.cursor()
    if request.method == "POST":
        titulo = request.form.get("titulocan")
        artista = request.form.get("artistacan")
        genero = request.form.get("generocan")
        precio = request.form.get("preciocan")
        duracion= request.form.get("duracioncan")
        lanzamiento = request.form.get("fechacan")
        imagen= request.form.get("imagencan")

        sql = "update canciones set titulo=%s, artista=%s,genero=%s,precio=%s, duracion=%s,lanzamiento=%s, img=%s where id_can=%s"
        cursor.execute(
            sql,
            (
                titulo,
                artista,
                genero,
                precio,
                duracion,
                lanzamiento,
                imagen,
                id
            ),
        )
        db.commit()

        return redirect(url_for("lista_cancion"))

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM canciones WHERE id_can=%s", (id,))
        data = cursor.fetchall()
        return render_template("actu_canciones.html", cancion=data[0])

if __name__ == "__main__":
    app.add_url_rule("/", view_func=lista)
    app.run(debug=True, port=5005)
