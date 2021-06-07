"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
connectionsfile = "connections.csv"
countriesfile = "countries.csv"
landingpfile = "landing_points.csv"
cont = None

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Crear el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Encontrar clusters dentro de la red y consultar conexión landing points")
    print("4- Encontrar puntos de interconexión en la red")
    print("5- Encontrar ruta mínima entre paises")
    print("6- Identificar infraestructura mínima")
    print("7- Identificar impacto de la caida de un landing point")
    print("8- Identificar ancho de banda máximo de un pais")
    print("0- Salir")
    print("*******************************************")
catalog = None

def optionTwo(cont):
    print("\nCargando información de los archivos ....")
    info = controller.loadData(cont, connectionsfile, countriesfile, landingpfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalVertexs(cont)
    numcountries = controller.totalCountries(cont)
    lp = info[0]
    c = info[1]
    print("\nInformación del primer landing point cargado:")
    print("Numero de identificación: " + lp['landing_point_id'])
    print("Identificador: " + lp['id'])
    print("Nombre: " + lp['name'])
    print("Latitud: " + str(lp['latitude']))
    print("Longitud: " + str(lp['longitude']))

    print("\nInformación del ultimo pais cargado:")
    print("Pais: " + c['CountryName'])
    print("Población: " + c['Population'])
    print("Numero de usuarios: " + c['Internet users'])

    print('\nNumero de landing points: ' + str(numvertex))
    print('Numero de cables: ' + str(numedges))
    print('Numero de paises: ' + str(numcountries))

def optionthree(cont, lp1, lp2):
    info = controller.clustersandlandingpoints(cont, lp1, lp2)
    clusters = info[0]
    connected = info[1]
    print("\nHay " + str(clusters) + " componentes conectados")
    if connected:
        print("Los landing points " + lp1 + " y " + lp2 + " estan en el mismo cluster")
    else:
        print("Los landing points " + lp1 + " y " + lp2 + " estan en el mismo cluster")

def optionfour(cont):
    info = controller.interconexions(cont)
    for i in lt.iterator(info):
        tot = str(i["total"])
        print("El landingpoint " + i["name"] + " con id " + str(i["id"]) + " del pais " + i["country"] + 
                " interconecta " + tot + " cables")
        
def optionfive(cont, p1, p2):
    info = controller.minroute(cont, p1, p2)
    totdis = info[1]
    path = info[0]
    print("\nLa distancia total del recorrido es: " + str(totdis) + " km")
    print("\nLa ruta mínima es: ")
    n = 1
    while st.isEmpty(path) == False:
        step = st.pop(path)
        print(str(n) + ". "+ step["vertexA"] + "-" + step["vertexB"] + ", Distancia: " + str(step["weight"]) + " km")
        n+=1

def optionsix(cont):
    info = controller.criticalstructure(cont)
    nodes = info[0]
    weight = info[1]
    #p#ath = info[2]
    print("\nLa red de expansión mínima cuenta con: " + str(nodes) + " nodos")
    print("\nEl costo total de la red es: " + str(weight) + " km")
    #print("\nLa rama mas larga del mst es: " + path)

def optionseven(cont, lp):
    info = controller.lpdamage(cont, lp)
    countries = info[0]
    num = info[1]
    print("\nCon la caida de este landing point se afectarian " + str(num) + " paises")
    print("\nEstos son: ")
    for i in lt.iterator(countries):
        print(i["country"] + ", Distancia: " + str(i["distance"]))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nCreando el catálogo de datos ....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        optionTwo(cont)

    elif int(inputs[0]) == 3:
        lp1 = input("Ingrese el primer landingpoint que desea consultar: ")
        lp2 = input("Ingrese el segundo landingpoint que desea consultar: ")
        optionthree(cont, lp1, lp2)

    elif int(inputs[0]) == 4:
        optionfour(cont)
    
    elif int(inputs[0]) == 5:
        p1 = input("Ingrese el primer pais que desea consultar: ").lower().replace(" ", "")
        p2 = input("Ingrese el segundo pais que desea consultar: ").lower().replace(" ", "")
        optionfive(cont)

    elif int(inputs[0]) == 6:
        optionsix(cont)

    elif int(inputs[0]) == 7:
        lp = input("Ingrese el nombre del landingpoint que desea consultar: ")
        optionseven(cont, lp)
    
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)
