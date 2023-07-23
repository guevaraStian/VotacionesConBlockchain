#Importamos la libreria matplotlib que nos ayuda a graficas
import matplotlib.pyplot as plt

#Solicitamos el maximo de candidatos, para asi configurar la veces que se repiten las preguntas
max_candidatos  = int(input(f"Por favor, Ingrese la cantidad maxima de candidatos al cargo : "))
"Declaramos 3 listas que nos serviran en este programa"
nombres_candidatos= []
cantidad_votos= []
porcentajes = [] 

#Con este for se guardan los nombres de los candidatos
for nom_candidato in range(max_candidatos):
    nom_candidato = input("Por favor, Ingrese nombre del candidato(a) : ")
    nombres_candidatos.append(nom_candidato)

#Con este for se guardan las cantidades de votos de cada candidato
for candidato in range(max_candidatos):
    votacion = int(input(f"Por favor,Ingrese la votación del candidato(a) {nombres_candidatos[candidato]}: "))
    cantidad_votos.append(votacion)

#obtenemos la sumatoria de la totalidad de los votos
total_votos = sum(cantidad_votos)
#las 2 siguientes impresiones en pantalla, separan el ingreso de la salida de datos
print("========================")
print("========================")
#En este for se calcula el porcentaje de cada candidato en votos sobre la cantidad total de ellos
for candidato in range(max_candidatos):
    porcentaje = 100 * cantidad_votos[candidato] / total_votos
    porcentajes.append(porcentaje)
    print(f"El candidato {nombres_candidatos[candidato]} tiene un porcentaje de {porcentaje:.2f}%")

#Imprimimos en pantalla 3 informaciones relacionadas a los datos ingresados
print(f"La cantidad de votos en total son : {total_votos}")
print(f"Los porcentajes de votacion por cada candidato son: {porcentajes}")
print("========================")
print("========================")
# Creamos un gráfica de barras, con la lista de nombres de candidatos y la cantidad de votos
fig, grafica = plt.subplots()
grafica.bar(x = nombres_candidatos, height = cantidad_votos, color='red')
plt.title('Grafica de candidatos por cantidad de votos', color = "red")
plt.show()
