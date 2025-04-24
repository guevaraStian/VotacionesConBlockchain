#Importamos la libreria matplotlib que nos ayuda a graficas
from flask import Flask, render_template, request, redirect, session, flash
#hash para la encriptacion de la cadena de bloques
import hashlib
#Se guarda en una base de datos mongodb
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import pymongo



app = Flask(__name__)

app.secret_key = b'\xaa\xe4V}y~\x84G\xb5\x95\xa0\xe0\x96\xca\xa7\xe7'

# Formulario para iniciar sesión


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def raiz_login():
    return render_template('login.html')

@app.route("/escritorio")
def escritorio():
    return render_template("escritorio.html")

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

@app.route("/formulario")
def upload_file():
    return render_template('formulario.html')



@app.route("/mostrar" , methods=['POST'])
#Luego de que activa el metodo 'POST' con la ruta "/mostrar" corre la siguiente funcion
def subirinfo():
    if request.method == 'POST':
        #Se conecta a la base de datos "Blockchain" y la coleccion "Bloques"
        client = MongoClient('localhost', port=27017, username='', password='')
        db = client['VBlockchain']
        col = db['Bloques']
        #Se consulta los bloques creados y se guarda en la variable "listabloques"
        listabloques = col.find()
        
    #Se publican las listas en el template verbloques.html
    return render_template('/verbloques.html', listabloques=listabloques)


# Manejar login
@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    correo = request.form["correo"]
    palabra_secreta = request.form["palabra_secreta"]
    # Aquí comparamos. Lo hago así de fácil por simplicidad
    # En la vida real debería ser con una base de datos y una contraseña hasheada
    if correo == "prueba@mail.com" and palabra_secreta == "123":
        # Si coincide, iniciamos sesión y además redireccionamos
        session["usuario"] = correo
        # Aquí puedes colocar más datos. Por ejemplo
        # session["nivel"] = "administrador"
        return redirect("/escritorio")
    else:
        # Si NO coincide, lo regresamos
        flash("Correo o contraseña incorrectos")
        return redirect("/login")




# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta != "/hacer_login" and ruta != "/logout" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar



#Este codigo se ejecuta cuando se activa guardar los datos
@app.route("/upload", methods=['POST'])
def uploader():
    if request.method == 'POST':
        #Se crean las variables y se guarda lo que viene del primer formulario
        nombre_1 = request.form['nombre_1']
        votacion_1 = request.form['votacion_1']
        nombre_2 = request.form['nombre_2']
        votacion_2 = request.form['votacion_2']
        #Conexion a la base de datos "Blockchain" y seleccion de la coleccion "Bloques"
        client = MongoClient('localhost', port=27017, username='', password='')
        db = client['VBlockchain']
        col = db['Bloques']

        #Se guarda en la variable "colvacia" si la coleccion "Bloques" esta vacia
        #colvacia = (col.count() == 0)
        colvacia = col.find_one({"NumeroBloque": "1"})
        
        #Si "colvacia" es "None" el HashAnterior es "Genesis" y el NumeroBloque es 1
        if(colvacia == None):
            HashAnterior = "Genesis"
            NumeroBloque = 1
            NumeroBloque = str(NumeroBloque)
            #Se encripta toda la informacion con sha256 anexando el hash
            encri = hashlib.sha256(NumeroBloque.encode()+nombre_1.encode()+votacion_1.encode()
                                   +nombre_2.encode()+votacion_2.encode()+HashAnterior.encode())
            HashActual = encri.hexdigest()
            #Se insertan los valores en la base de datos
            col.insert_one({'NumeroBloque': NumeroBloque, 'nombre_1': nombre_1, 'votacion_1': votacion_1,
                        'nombre_2': nombre_2, 'votacion_2': votacion_2, 'HashAnterior': HashAnterior, 'HashActual': HashActual 
            })
        
        #Si "colvacia" es DIFERENTE de "None" el HashAnterior es varia y el NumeroBloque es depende de cuantos se hayan creado
        if (colvacia != None):
            #Se guarda en la variable "bloquecodificado" el ultimo bloque que se inserto
            bloquecodificado = col.find().sort('NumeroBloque', -1).limit(1)
            #se recorren los items dentro de ese ultimo bloque 
            #cada item se guarda en la variable "bloqueanterior"
            for item in bloquecodificado :
                bloqueanterior = item
            #Dentro de la lista que se guardo en "bloqueanterior" se selecciona el campo "NumeroBloque"
            numbloqant = bloqueanterior['NumeroBloque']
            #Dentro de la lista que se guardo en "bloqueanterior" se selecciona el campo "HashActual"
            hashbloqant = bloqueanterior['HashActual']
            numbloqant= int(numbloqant)
            NumeroBloque = numbloqant + 1
            HashAnterior = hashbloqant
            #Se convierten las variables en string para poderla guardar en la base de datos
            NumeroBloque = str(NumeroBloque)
            HashAnterior = str(HashAnterior)
            #Se encripta la informacion
            encri = hashlib.sha256(NumeroBloque.encode()+nombre_1.encode()+votacion_1.encode()+nombre_2.encode()
                               + votacion_2.encode()+HashAnterior.encode())
            HashActual = encri.hexdigest()
            #Se insertan los valores en la base de datos
            col.insert_one({'NumeroBloque': NumeroBloque, 'nombre_1': nombre_1, 'votacion_1': votacion_1,
                        'nombre_2': nombre_2, 'votacion_2': votacion_2, 'HashAnterior': HashAnterior, 'HashActual': HashActual
            })
        #En formulario se retorna e imprime en pantalla la siguiente informacion
        return render_template('formulario.html', NumeroBloque=NumeroBloque,nombre_1=nombre_1, votacion_1= votacion_1,
                               nombre_2= nombre_2 , votacion_2= votacion_2,HashAnterior=HashAnterior, HashActual=HashActual )


###############
# Codigo nuevo de voto individual
##############

@app.route("/realizar_votacion")
def realizar_votacion():
    return render_template('realizar_votacion.html')



@app.route("/crear_voto", methods=['POST'])
def crear_votoder():
    if request.method == 'POST':
        #Se crean las variables y se guarda lo que viene del primer formulario
        numero_cedula = request.form['numero_cedula']
        nombre_votante = request.form['nombre_votante']
        voto_pais = request.form['voto_pais']
        voto_departamento = request.form['voto_departamento']
        voto_municipio = request.form['voto_municipio']

        #Conexion a la base de datos "Blockchain" y seleccion de la coleccion "Bloques"
        client = MongoClient('localhost', port=27017, username='', password='')
        db = client['VBlockchain']
        col = db['Bloques_votos_individuales']

        #Se guarda en la variable "colvacia" si la coleccion "Bloques" esta vacia
        #colvacia = (col.count() == 0)
        colvacia = col.find_one({"NumeroBloque": "1"})
        
        #Si "colvacia" es "None" el HashAnterior es "Genesis" y el NumeroBloque es 1
        if(colvacia == None):
            HashAnterior = "Genesis"
            NumeroBloque = 1
            NumeroBloque = str(NumeroBloque)
            #Se encripta toda la informacion con sha256 anexando el hash
            encri = hashlib.sha256(NumeroBloque.encode()+numero_cedula.encode()+nombre_votante.encode()
                                   +voto_pais.encode()+voto_departamento.encode()+voto_municipio.encode()+HashAnterior.encode())
            HashActual = encri.hexdigest()
            #Se insertan los valores en la base de datos
            col.insert_one({'NumeroBloque': NumeroBloque, 'numero_cedula': numero_cedula, 'nombre_votante': nombre_votante,
                        'voto_pais': voto_pais, 'voto_departamento': voto_departamento, 'voto_municipio': voto_municipio, 'HashAnterior': HashAnterior, 'HashActual': HashActual 
            })
        
        #Si "colvacia" es DIFERENTE de "None" el HashAnterior es varia y el NumeroBloque es depende de cuantos se hayan creado
        if (colvacia != None):
            #Se guarda en la variable "bloquecodificado" el ultimo bloque que se inserto
            bloquecodificado = col.find().sort('NumeroBloque', -1).limit(1)
            #se recorren los items dentro de ese ultimo bloque 
            #cada item se guarda en la variable "bloqueanterior"
            for item in bloquecodificado :
                bloqueanterior = item
            #Dentro de la lista que se guardo en "bloqueanterior" se selecciona el campo "NumeroBloque"
            numbloqant = bloqueanterior['NumeroBloque']
            #Dentro de la lista que se guardo en "bloqueanterior" se selecciona el campo "HashActual"
            hashbloqant = bloqueanterior['HashActual']
            numbloqant= int(numbloqant)
            NumeroBloque = numbloqant + 1
            HashAnterior = hashbloqant
            #Se convierten las variables en string para poderla guardar en la base de datos
            NumeroBloque = str(NumeroBloque)
            HashAnterior = str(HashAnterior)
            #Se encripta la informacion
            encri = hashlib.sha256(NumeroBloque.encode()+numero_cedula.encode()+nombre_votante.encode()
                                   +voto_pais.encode()+voto_departamento.encode()+voto_municipio.encode()+HashAnterior.encode())
            HashActual = encri.hexdigest()
            #Se insertan los valores en la base de datos
            col.insert_one({'NumeroBloque': NumeroBloque, 'numero_cedula': numero_cedula, 'nombre_votante': nombre_votante,
                        'voto_pais': voto_pais, 'voto_departamento': voto_departamento, 'voto_municipio': voto_municipio, 'HashAnterior': HashAnterior, 'HashActual': HashActual 
            })
        #En formulario se retorna e imprime en pantalla la siguiente informacion
        return render_template('realizar_votacion.html',NumeroBloque= NumeroBloque, numero_cedula=numero_cedula,nombre_votante=nombre_votante, voto_pais= voto_pais,
                               voto_departamento= voto_departamento , voto_municipio= voto_municipio,HashAnterior=HashAnterior, HashActual=HashActual )


@app.route("/mostrar_voto_individual" , methods=['POST'])
#Luego de que activa el metodo 'POST' con la ruta "/mostrar" corre la siguiente funcion
def subirinfovoto():
    if request.method == 'POST':
        #Se conecta a la base de datos "Blockchain" y la coleccion "Bloques"
        client = MongoClient('localhost', port=27017, username='', password='')
        db = client['VBlockchain']
        col = db['Bloques_votos_individuales']
        #Se consulta los bloques creados y se guarda en la variable "listabloques"
        listabloques_indv = col.find()
        
    #Se publican las listas en el template verbloques.html
    return render_template('/ver_votos_individuales.html', listabloques_indv=listabloques_indv)


###############
# Codigo nuevo  de voto individual
##############

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)




