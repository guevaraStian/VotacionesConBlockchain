#Importamos la libreria matplotlib que nos ayuda a graficas
import matplotlib.pyplot as plt

# Libreria de FASK sive para
import os
from flask import Flask, render_template, request, abort, jsonify

#hash para la encriptacion de la cadena de bloques
import hashlib
#Se guarda en una base de datos mongodb
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import pymongo


#Se inicia flask
app = Flask(__name__)
#Se agregan las rutas de cada opcion de las plantillas html o templates
@app.route("/")
def upload_file():
    return render_template('formulario.html')

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

@app.route("/mostrar", methods=['POST'])
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
    return render_template('verbloques.html', listabloques=listabloques)
        


if __name__ == '__main__':
    app.run(debug=True)


