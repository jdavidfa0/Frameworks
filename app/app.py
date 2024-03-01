from flask import Flask, render_template, request, url_for, redirect

import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="agenda"
)

cursor = db.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrar", methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == "POST":
        nombre = request.form.get("Nombreper")
        apellido = request.form.get("apellidoper")
        correo = request.form.get("emailper")
        direccion = request.form.get("dirreccionper")
        telefono = request.form.get("telefonoper")
        usuario = request.form.get("usuarioper")
        contrasena = request.form.get("contraper")

        # insertar datos a la tabla persona
        cursor.execute(
            "insert into personas( Nombreper ,apellidoper ,emailper ,dirreccionper ,telefonoper ,usuarioper ,contraper )values(%s,%s,%s,%s,%s,%s,%s)",
            (nombre, apellido, correo, direccion, telefono, usuario, contrasena)
            
        )
        db.commit()

        return redirect(url_for("registrar_usuario"))
    
    return render_template("Registrar.html")


if __name__ == "__main__":
    app.add_url_rule("/", view_func=index)
    app.run(debug=True, port=5005)
