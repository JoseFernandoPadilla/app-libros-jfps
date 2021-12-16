from flask import Flask, render_template, redirect, request #Importamos la clase de Flasck
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from sqlalchemy.orm import query
#from werkzeug.utils import redirect
#https://github.com/JoseFernandoPadilla/app-libros-jfps.git
#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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:FPadilla@localhost:5432/bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class usuarios(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email=email
        self.password=password

class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial=nombre_editorial

class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas =db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    #Relacion
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen,id_editorial, id_genero, id_autor):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_autor = id_autor
        self.id_editorial = id_editorial
        self.id_genero = id_genero

class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(100))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))


    def __init__(self, nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(100))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

class Favoritos(db.Model):
    __tablename__ = "favoritos"
    id_lista_favoritos = db.Column(db.Integer, primary_key=True)

    #Relacion
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    

    def __init__(self, id_libro, id):
        self.id_libro = id_libro
        self.id = id

@app.route("/favoritos")
def favoritos():
    consulta_favoritos = Favoritos.query.all()
    consulta_libro = Libro.query.all()
    consulta_usuario = usuarios.query.all()
    for favoritos in consulta_favoritos:
        id_libro = favoritos.id_libro
        id = favoritos.id
    return render_template("favoritos.html",usuarios = consulta_usuario, favoritos = consulta_favoritos, libros = consulta_libro)

@app.route("/agregar_favorito/<id>")
def agregar_favorito(id):
    libro = Libro.query.filter_by(id_libro=int(id)).first()
    fav = Favoritos(libro.id_libro, 1)
    db.session.add(fav)
    db.session.commit()
    return redirect("/tablaLibro")

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    #password_cifrado = bcrypt.generate_password_hash(password)
    consulta_usuarios = usuarios.query.filter_by(email=email).first()
    print(consulta_usuarios.email)
    bcrypt.check_password_hash(consulta_usuarios.password,password)

    return "Hizo click en botoin login"

@app.route("/registrar")
def registrar():
    #return "Hizo click en boton hiperbinculo registrar"
    return render_template("registro.html")

@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)

    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)

    usuario = usuarios(email=email, password = password_cifrado)
    db.session.add(usuario)
    db.session.commit()
    #crear el objeto de tipo usuario
    #con comntrseña cifrada
    #y alamcenar en base de datos
    return redirect ("/")

@app.route("/iniciar_sesion")
def iniciar_sesion():
    redirect("/")

@app.route("/libro")
def libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("libro.html", consulta_editorial=consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)

@app.route("/registrarLibro", methods=["POST"])
def registrarLibro():
    #codigo para guardar el libro en la base de datos 
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    id_editorial = request.form["editorial"] 
    id_autor = request.form["autor"]
    id_genero = request.form["genero"]
    numero_paginas_int = int(numero_paginas)

    libro_nuevo = Libro(titulo_libro= titulo_libro, fecha_publicacion=fecha_publicacion, numero_paginas=numero_paginas_int, formato=formato, volumen=volumen, id_editorial=id_editorial, id_genero=id_genero, id_autor=id_autor)
    db.session.add(libro_nuevo)
    db.session.commit()
    message= "Libro registrado"
    return redirect ("/tablaLibro")

#Modificar editorial la funcion def para que sea para editorial ahorita tiene la de libro
@app.route("/editorial")
def editorial():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("editorial.html", consulta_editorial=consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)


@app.route("/registrarEditorial", methods=["POST"])
def registrarEditorial():
    #codigo para guardar la editorial en la base de datos
    nombre_editorial = request.form["nombre_editorial"]

    editorial_nuevo = Editorial(nombre_editorial=nombre_editorial)
    db.session.add(editorial_nuevo)
    db.session.commit()
    message= "Editorial registrado"
    return redirect ("/tablaEditorial")

@app.route("/autor")
def autor():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("autor.html", consulta_editorial=consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)


@app.route("/registrarAutor", methods=["POST"])
def registrarAutor():
    #codigo para guardar el autor
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]

    autor_nuevo = Autor(nombre_autor=nombre_autor, fecha_nac=fecha_nac, nacionalidad=nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    message="Autor nuevo"
    return redirect ("/tablaAutor")

@app.route("/genero")
def genero():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    return render_template("genero.html", consulta_editorial=consulta_editorial, consulta_genero = consulta_genero, consulta_autor = consulta_autor)


@app.route("/registrarGenero", methods=["POST"])
def registrarGenero():
    #codigo para guardar el genero en la base de datos 
    nombre_genero = request.form["nombre_genero"]

    genero_nuevo = Genero(nombre_genero=nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    message="Genero nuevo"
    print("Agregado")
    return redirect ("/tablaGenero")

#---Funciones de crear y mostrar en una tabla los objetos guardados------

@app.route("/tablaGenero")
def tabalaGenero():
    consulta_genero = Genero.query.all()
    return render_template("tablaGenero.html", genero = consulta_genero)

@app.route("/tablaEditorial")
def tabalaEditorial():
    consulta_genero = Editorial.query.all()
    return render_template("tablaEditorial.html", editorial = consulta_genero)

@app.route("/tablaAutor")
def tabalaAutor():
    consulta_autor = Autor.query.all()
    return render_template("tablaAutor.html", autor = consulta_autor)

@app.route("/tablaLibro")
def tablaLibro():
    consulta_libro = Libro.query.all()
    return render_template("tablaLibro.html", libro = consulta_libro)

#---------Funciones de Eliminar---------#
@app.route("/eliminarEditorial/<idE>")
def eliminarEditorial(idE):
    Editorial.query.filter_by(id_editorial=int(idE)).delete()
    #print(editorial)
    db.session.commit()
    return render_template("editorial.html")

@app.route("/eliminarLibro/<idL>")
def eliminarLibro(idL):
    Libro.query.filter_by(id_libro =int(idL)).delete()
    #print(editorial)
    db.session.commit()
    return render_template("tablaLibro.html")

@app.route("/eliminarAutor/<idA>")
def eliminarAutor(idA):
    Autor.query.filter_by(id_autor =int(idA)).delete()
    #print(editorial)
    db.session.commit()
    return render_template("tablaAutor.html")

@app.route("/eliminarGenero/<idG>")
def eliminarGenero(idG):
    Genero.query.filter_by(id_genero =int(idG)).delete()
    #print(editorial)
    db.session.commit()
    return render_template("tablaGenero.html")

#--------Funciones de Modificar o Editar ---------

@app.route("/editarEditorial/<idE>")
def editarEditorial(idE):
    editorial = Editorial.query.filter_by(id_editorial=int(idE)).first()
    print(editorial)
    print(editorial.nombre_editorial)
    return render_template("editarEditorial.html", editorial=editorial)

@app.route("/EditarEditorial", methods=['POST'])
def EditarEditorial():
    id_editorial = request.form['idEditorial']
    Nuevo_nombre_editorial= request.form['Nombre_editorial']
    editorial = Editorial.query.filter_by(id_editorial=int(id_editorial)).first()
    editorial.nombre_editorial = Nuevo_nombre_editorial
    db.session.commit()
    return render_template("tablaEditorial.html")

@app.route("/editarLibro/<idL>")
def editarLibro(idL):
    libro = Libro.query.filter_by(id_libro =int(idL)).first()
    print(libro)
    print(libro.titulo_libro)
    print(libro.fecha_publicacion)
    print(libro.numero_paginas)
    print(libro.formato)
    print(libro.volumen)
    return render_template("editarLibro.html", libro=libro)

@app.route("/EditarLibro", methods=['POST'])
def EditarLibro():
    id_libro = request.form['idLibro']
    Nuevo_titulo_libro= request.form['titulo_libro']
    Nuevo_fecha_libro= request.form['fecha_publicacion']
    Nuevo_numerop_libro= request.form['numero_paginas']
    Nuevo_formato_libro= request.form['formato']
    Nuevo_volumen_libro= request.form['volumen']
    libro = Libro.query.filter_by(id_libro=int(id_libro)).first()
    libro.titulo_libro = Nuevo_titulo_libro
    libro.fecha_publicacion = Nuevo_fecha_libro
    libro.numero_paginas = Nuevo_numerop_libro
    libro.formato = Nuevo_formato_libro
    libro.volumen = Nuevo_volumen_libro
    db.session.commit()
    return render_template("tablaLibro.html")
    
@app.route("/editarAutor/<idA>")
def editarAutor(idA):
    autor = Autor.query.filter_by(id_autor =int(idA)).first()
    print(autor)
    print(autor.nombre_autor)
    print(autor.fecha_nac)
    print(autor.nacionalidad)
    return render_template("editarAutor.html", autor=autor)

@app.route("/EditarAutor", methods=['POST'])
def EditarAutor():
    id_autor = request.form['idAutor']
    Nuevo_nombre_autor= request.form['nombre_autor']
    Nuevo_fecha_nac= request.form['fecha_nac']
    Nuevo_nacionalidad= request.form['nacionalidad']
    autor = Autor.query.filter_by(id_autor=int(id_autor)).first()
    autor.nombre_autor = Nuevo_nombre_autor
    autor.fecha_nac = Nuevo_fecha_nac
    autor.nacionalidad = Nuevo_nacionalidad
    db.session.commit()
    return render_template("tablaAutor.html")

@app.route("/editarGenero/<idG>")
def editarGenero(idG):
    genero = Genero.query.filter_by(id_genero =int(idG)).first()
    print(genero)
    print(genero.nombre_genero)
    return render_template("editarGenero.html", genero=genero)

@app.route("/EditarGenero", methods=['POST'])
def EditarGenero():
    id_genero = request.form['idGenero']
    Nuevo_nombre_genero= request.form['nombre_genero']
    genero = Genero.query.filter_by(id_genero=int(id_genero)).first()
    genero.nombre_genero = Nuevo_nombre_genero
    db.session.commit()
    return render_template("tablaGenero.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)