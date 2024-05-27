from flask import Flask,  jsonify, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import base64

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


@app.route("/lista")
def lista():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM personas")
    usuario = cursor.fetchall()
    return render_template("index.html", personas=usuario)

@app.route("/Lista_canciones", methods=["GET", "POST"])
def lista_cancion():
    cursor= db.cursor()
    cursor.execute("SELECT id_can, titulo, artista, genero, precio, duracion, lanzamiento, img FROM canciones")
    canciones = cursor.fetchall()

    if canciones:
        cancioneslista=[]
        for cancion in canciones:

            imagen=base64.b64encode(cancion[7]).decode('utf-8')

            cancioneslista.append({
                'id_can': cancion[0],
                'titulo': cancion[1],
                'artista': cancion[2],
                'genero': cancion[3],
                'precio': cancion[4],
                'duracion': cancion[5],
                'lanzamiento': cancion[6],
                'imagen':imagen
            })
        
        return render_template("Lista_canciones.html", canciones=cancioneslista)
    else:
        return render_template("Lista_canciones.html")
   
@app.route("/Lista_canciones_u", methods=["GET", "POST"])
def lista_cancion_u():
    cursor= db.cursor()
    cursor.execute("SELECT id_can, titulo, artista, genero, precio, duracion, lanzamiento, img FROM canciones")
    canciones = cursor.fetchall()

    if canciones:
        cancioneslista=[]
        for cancion in canciones:

            imagen=base64.b64encode(cancion[7]).decode('utf-8')

            cancioneslista.append({
                'id_can': cancion[0],
                'titulo': cancion[1],
                'artista': cancion[2],
                'genero': cancion[3],
                'precio': cancion[4],
                'duracion': cancion[5],
                'lanzamiento': cancion[6],
                'imagen':imagen
            })
        
        return render_template("lista_cancion_u.html", canciones=cancioneslista)
    else:
        return render_template("lista_cancion_u.html")

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
        rol = request.form.get("rolregistrar")
        
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
                "insert into personas( Nombreper ,apellidoper ,emailper ,dirreccionper ,telefonoper ,usuarioper ,contraper, roles )values(%s,%s,%s,%s,%s,%s,%s,%s)",
                (nombre, apellido, correo, direccion, telefono, usuario, contrasenaencriptada, rol),
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
        username=request.form.get('usuarioinir')
        password= request.form.get('contraini')

        cursor=db.cursor(dictionary=True)
        cursor.execute("SELECT usuarioper, contraper, roles from personas WHERE usuarioper=%s", (username,))
        resultado=cursor.fetchone()

       
        if resultado and check_password_hash(resultado['contraper'],password):
            session['usuario']=username
            session['usuario'] = resultado ['usuarioper']
            session['rol'] = resultado['roles']
        # De acuerdo al rol asignamos la url 
            if resultado ['roles'] == 'admin':
                return redirect (url_for ('lista'))
            else:
                return redirect (url_for ('lista_cancion_u'))
        
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
        imagen= request.files["imagencan"]

        imagen2= imagen.read()
        
        cursor.execute("insert into canciones( titulo,artista ,genero,precio,duracion ,lanzamiento ,img)values(%s,%s,%s,%s,%s,%s,%s)",
        (titulo, artista, genero, precio, duracion,lanzamiento, imagen2),)
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
        imagen= request.files["imagencan"]
        imagen2= imagen.read()
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
                imagen2,
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
    

@app.route('/agregar_carrito', methods=['GET', 'POST'])
def agregar_carrito():
  
    idcan= request.form['id']
    titulocan= request.form['titulo']
    preciocan=request.form['precio']

    if 'cart' not in session:
        session['cart']=[]
    
    session['cart'].append({'id':idcan, 'titulo':titulocan,'precio': float(preciocan)})
    session.modified =True

    print("contenido del carro", session['cart'])

    return jsonify({'message':'Cancion agregada al carro'})

@app.route('/eliminar_uno', methods=['POST'])
def eliminar_uno():
    print('AUXILIO')

    idcan=request.form.get('id')
    print(idcan)
    
    if 'cart' in session:
        carrito =session['cart']
        for item in carrito:
            if item['id'] == idcan:

                carrito.remove(item)
                print(carrito)

                session['cart'] =carrito

                session.modified = True
                return jsonify({'message':'Cancion eliminada del carro'})
    return jsonify({'error':'Elemento no econtrado'})




@app.route('/carrito', methods=['GET', 'POST'])
def ver_carrito():
    
    carro= session.get('cart', [])
    total= sum(item['precio'] for item in carro )
    print(session['cart'])
    return render_template('carrito.html', carro=carro, total=total)



@app.route('/eliminar_carrito', methods=['GET', 'POST'])
def limpiar():
    session['cart'].clear()
    session.modified =True
    
    return render_template('carrito.html')






if __name__ == "__main__":
    app.add_url_rule("/", view_func=login)
    app.run(debug=True, port=5005)
