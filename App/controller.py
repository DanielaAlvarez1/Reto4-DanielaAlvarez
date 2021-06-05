"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadData(cont, connectionsfile, countriesfile, landingpfile):
    lp = loadLandingPoints(cont, landingpfile)
    loadConnections(cont, connectionsfile)
    c = loadCountries(cont, countriesfile)
    return (lp, c)

def loadLandingPoints(cont, landingpfile):
    cfile = cf.data_dir + landingpfile
    input_file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    a = ""
    for i in input_file:
        if a == "":
            a = i
        model.addLandingPointHash(cont, i)

    return a

def loadConnections(cont, connectionsfile):
    cfile = cf.data_dir + connectionsfile
    input_file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    for i in input_file:
        model.addConnection(cont, i)

def loadCountries(cont, countriesfile):
    cfile = cf.data_dir + countriesfile
    input_file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    a = 1
    b = {}
    for i in input_file:
        model.addCountry(cont, i)
        a+=1
        if a == 239:
            b = i

    return b

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalVertexs(analyzer):
    return model.totalVertexs(analyzer)

def totalConnections(analyzer):
    return model.totalConnections(analyzer)

def totalCountries(analyzer):
    return model.totalCountries(analyzer)

def clustersandlandingpoints(cont, lp1, lp2):
    return model.clustersandlandingpoints(cont, lp1, lp2)