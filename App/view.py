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
    controller.loadData(cont, connectionsfile, countriesfile, landingpfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    numcountries = controller.totalCountries(cont)
    print('Numero de landing points: ' + str(numvertex))
    print('Numero de cables: ' + str(numedges))
    print('Numero de paises: ' + str(numcountries))

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
        pass

    elif int(inputs[0]) == 4:
        pass
    
    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass
    
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)
