from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost", user="root", password="", database="agenda"
)

cursor = db.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Registrar", methods=["POST"])
def registrar_usuario():
    nombre = (request.form["Nombreper"],)
    apellido = (request.form["apellidoper"],)
    correo = (request.form["emailper"],)
    dirrecion = (request.form["direccionper"],)
    telefono = (request.form["telefonoper"],)
    usuario = (request.form["usuarioper"],)
    contrasena = request.form["contraper"]

    # insertar datos a la tabla persona
    cursor.execute(
        "insert into personas (Nombreper,apellidoper,emailper,direccionper,telefonoper,usuarioper,contraper)values(%s,%s,%s,%s,%s,%s,%s)",
        (nombre, apellido, correo, dirrecion, telefono, usuario, contrasena),
    )
    db.commit()

    return redirect(url_for("Registrar"))


if __name__ == "__main__":
    app.add_url_rule("/", view_func=index)
    app.run(debug=True, port=5005)
