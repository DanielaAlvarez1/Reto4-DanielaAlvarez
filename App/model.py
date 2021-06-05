﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import name
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer = {
                'countries': None,
                'landing_points': None,
                'countries_cables': None,
                'capacity': None,
                'cables': None,
                }
    """
    Se carga en una tabla de Hash el archivo de countries
    Llave: Nombre
    Valor: Diccionario con su información
    """
    analyzer['countries'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareValue)

    """
    Se almacena en una tabla de Hash todos los cables que llegan a los paises
    Llave: Nombre Pais
    Valor: Lista de diccionarios de las conecciones
            {"nombre conexion", "capacidad", "nombre vertice"}
    """
    analyzer['countries_cables'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareValue)   

    """
    Se almacena la capacidad de cada conexion en una tabla de Hash
    Llave: Nombre conexion (origen-destino-cable)
    Valor: Capacidad
    """ 

    analyzer['capacity'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareValue)

    """
    Se carga en una table de Hash el archivo de landing-points
    Llave: Id landing point(numero)
    Valor: Diccionario con la información
    """
    analyzer['landing_points'] = mp.newMap(numelements=1400,
                                     maptype='PROBING',
                                     comparefunction=compareValue)

    """
    Se carga en una table de Hash las conexiones de un landing point
    Llave: Nombre landing point
    Valor: Lista de vertices
    """
    analyzer['landing_points_cables'] = mp.newMap(numelements=1400,
                                     maptype='PROBING',
                                     comparefunction=compareValue)

    """
    Se carga en un grafo las conecciones entre landing points
    Vertices: <Nombre Landing Point>-<Nombre cable>
    """
    analyzer['cables'] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=14000,
                                    comparefunction=compareLPs)

    return analyzer

# Funciones para agregar informacion al catalogo
def addLandingPointHash(analyzer, dic):
    mp.put(analyzer["landing_points"], int(dic["landing_point_id"]), dic)
    return analyzer
    
def addConnection(analyzer, dic):
    cable = dic["cable_name"]
    origin = formatVertex(analyzer, dic['\ufefforigin'], cable)
    destination = formatVertex(analyzer, dic["destination"], cable)
    d = dic["cable_length"].replace(" km", "")
    if 'n.a.' in d:
        distance = 0
    else:
        distance = float(d.replace(",", ""))
    addLandingPoint(analyzer, origin)
    addLandingPoint(analyzer, destination)
    addCable(analyzer, origin, destination, distance)
    connection = origin + destination + cable
    capacity = float(dic["capacityTBPS"])
    addCapacity(analyzer, connection, capacity)
    addCountryLandingPoint(analyzer, dic, destination, connection, capacity)
    return analyzer

def addCountry(analyzer, dic):
    mp.put(analyzer["countries"], dic["CountryName"], dic)
    return analyzer

# Funciones de interacción entre estructuras
def getLandingPointInfo(analyzer, lpid):
    map = analyzer['landing_points']
    a = mp.get(map, int(lpid))
    info = me.getValue(a)
    return info 

# Funciones para creacion de datos
def formatVertex(analyzer, landingpoint, cable):
    lpinfo = getLandingPointInfo(analyzer, landingpoint)
    lpname = lpinfo["name"].split(",")[0]
    name = lpname + '-' + cable
    addVertexLandingPoint(analyzer, lpname, name)
    return name

def addVertexLandingPoint(analyzer, lpname, name):
    if mp.contains(analyzer["landing_points_cables"], lpname):
        a = mp.get(analyzer["landing_points_cables"], lpname)
        lplist = me.getValue(a)
    else:
        lplist = lt.newList(datastructure= "ARRAY_LIST")
    if lt.isPresent(lplist, name) == 0:
        lt.addLast(lplist, name)
        mp.put(analyzer["landing_points_cables"], lpname, lplist)

def addLandingPoint(analyzer, landingpoint):
    if not gr.containsVertex(analyzer["cables"], landingpoint):
        gr.insertVertex(analyzer["cables"], landingpoint)
    return analyzer

def addCable(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['cables'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['cables'], origin, destination, distance)
    return analyzer

def addCapacity(analyzer, connection, capacity):
    mp.put(analyzer["capacity"], connection, capacity)
    return analyzer

def addCountryLandingPoint(analyzer, landingpoint, lpvertex, connection, capacity):
    lpinfo = getLandingPointInfo(analyzer, landingpoint["destination"])
    lpname = lpinfo["name"].split(",")
    namesize = len(lpname)
    
    if namesize == 3:
        country = lpname[2].lower().replace(" ", "")
    elif namesize == 2:
        country = lpname[1].lower().replace(" ", "")
    else:
        country = "No identified"
    if mp.contains(analyzer['countries_cables'], country):
        a = mp.get(analyzer['countries_cables'], country)
        countrylist = me.getValue(a)
    else:
        countrylist = lt.newList(datastructure= 'ARRAY_LIST')
    lt.addLast(countrylist, {"name": connection, "capacity": capacity, "vertex": lpvertex})

    min = 1000000000000000
    for i in lt.iterator(countrylist):
        if i["capacity"] < min:
            min = i["capacity"]

    for i in lt.iterator(countrylist):         
        if i["vertex"] != lpvertex:
            addCable(analyzer, lpvertex, i["vertex"], 0.1)
            connection = lpvertex + i["vertex"] + "IC"
            addCapacity(analyzer, connection, min)

    mp.put(analyzer['countries_cables'], country, countrylist)

    return analyzer

# Funciones de consulta
def totalVertexs(analyzer):
    return gr.numVertices(analyzer['cables'])

def totalConnections(analyzer):
    return gr.numEdges(analyzer['cables'])

def totalCountries(analyzer):
    return mp.size(analyzer['countries'])

def clustersandlandingpoints(analyzer, lp1, lp2):
    analyzer['components'] = scc.KosarajuSCC(analyzer['cables'])
    clusters = scc.connectedComponents(analyzer['components'])
    a = mp.get(analyzer["landing_points_cables"], lp1)
    lp1list = me.getValue(a)
    b = mp.get(analyzer["landing_points_cables"], lp2)
    lp2list = me.getValue(b)
#    prueba(analyzer)

    for i in lt.iterator(lp1list):
        for e in lt.iterator(lp2list):
            connected = scc.stronglyConnected(analyzer['components'], i, e)
            if connected:
                break 
            
    return (clusters, connected)

def interconexions(analyzer):
    lps = mp.keySet(analyzer["landing_points"])
    lpslist = lt.newList(datastructure= "ARRAY_LIST")
    for i in lt.iterator(lps):
        dic = {}
        dic["id"] = i
        a = mp.get(analyzer["landing_points"], i)
        lpinfo = me.getValue(a)
        dic["name"] = lpinfo["name"]
        namelist = dic["name"].split(",")
        if len(namelist) == 3:
            dic["country"] = namelist[2]
        if len(namelist) == 2:
            dic["country"] = namelist[1]
        else:
            dic["country"] = namelist[0]
        b = mp.get(analyzer["landing_points_cables"], namelist[0])
        lplist = me.getValue(b)
        if lt.size(lplist) > 1:
            dic["total"] = str(lt.size(lplist))
            lt.addLast(lpslist, dic)

    return lpslist

def prueba(analyzer):
    b = mp.get(analyzer["landing_points_cables"], "Vung Tau")
    lp2list = me.getValue(b)
    for i in lt.iterator(lp2list):
        print(i)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareLPs(lp, keyvaluestop):
    lpcode = keyvaluestop['key']
    if (lp == lpcode):
        return 0
    elif (lp > lpcode):
        return 1
    else:
        return -1

def compareValue(val1, val2):
    if (val1 == val2):
        return 1
    else:
        return 0

def compareCapacity(lp1, lp2):
    if lp1["capacity"] > lp2["capacity"]:
        return True
    else:
        return False

# Funciones de ordenamiento
def sort(lst, comparefunction):
    sorted_list = sa.sort(lst, comparefunction)
    return sorted_list
