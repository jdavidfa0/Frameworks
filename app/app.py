from flask import Flask, render_template, request, url_for, redirect, flash, session
import bcrypt
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost", user="root", password="", database="agenda"
)

cursor = db.cursor()

def encriptarcontra(contraencrip):
    encriptar= bcrypt.hashpw(contraencrip.encode('utf-8'), bcrypt.gensalt())
    return encriptar


@app.route("/")
def lista():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM personas")
    usuario = cursor.fetchall()
    return render_template("index.html", personas=usuario)


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
        
        contrasenaencriptada=encriptarcontra(contrasena)

        cursor.execute('SELECT * FROM personas WHERE usuarioper=%s',(usuario,))
        resultado1=cursor.fetchall()
        cursor.execute('SELECT * FROM personas WHERE emailper=%s',(correo,))
        resultado2=cursor.fetchall()
        
    
        if len(resultado1)>0 or len(resultado2)>0:
            return redirect(url_for('usuario_existe'))
        else:
    # insertar datos a la tabla persona
            cursor.execute(
                "insert into personas( Nombreper ,apellidoper ,emailper ,dirreccionper ,telefonoper ,usuarioper ,contraper )values(%s,%s,%s,%s,%s,%s,%s)",
                (nombre, apellido, correo, direccion, telefono, usuario, contrasenaencriptada),
            )
            db.commit()
            #flash("usuario creado correctamente", "sucess")

            return redirect(url_for("registrar_usuario"))

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
        username=request.form.get('usuarioini')
        password= request.form.get('contraini')

        cursor=db.cursor()
        cursor.execute('SELECT usuarioper, contraper from personas WHERE usuarioper=%s', (username,))
        usuarios=cursor.fetchone()
       
        if usuarios and bcrypt.check_password_hash(usuarios[7], password):
            session['usuario']=username
            return redirect(url_for('lista'))
        else:
            error='Credenciales invalidas, intente denuevo'
            return render_template('login.html', error=error)
    return render_template('login.html')

    
    


if __name__ == "__main__":
    app.add_url_rule("/", view_func=lista)
    app.run(debug=True, port=5005)
