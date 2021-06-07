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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.ADT.indexminpq import size
from os import name
from math import radians, cos, sin, asin, sqrt
from random import randint
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import stack as st
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import bellmanford as bf
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
    dic["latitude"] = float(dic["latitude"])
    dic["longitude"] = float(dic["longitude"])
    mp.put(analyzer["landing_points"], int(dic["landing_point_id"]), dic)
    return analyzer
    
def addConnection(analyzer, dic):
    cable = dic["cable_name"]
    origin = formatVertex(analyzer, dic['\ufefforigin'], cable)
    destination = formatVertex(analyzer, dic["destination"], cable)
    origindic = getLandingPointInfo(analyzer, dic['\ufefforigin'])
    destinationdic = getLandingPointInfo(analyzer, dic["destination"])
    lon1 = origindic["longitude"]
    lat1 = origindic["latitude"]
    lon2 = destinationdic["longitude"]
    lat2 = destinationdic["latitude"]
    distance = haversine(lon1, lat1, lon2, lat2)
    addLandingPoint(analyzer, origin)
    addLandingPoint(analyzer, destination)
    addCable(analyzer, origin, destination, distance)
    connection = origin + destination + cable
    capacity = float(dic["capacityTBPS"])
    destinationdic["destination"] = destination
    addCapacity(analyzer, connection, capacity)
    addCountryLandingPoint(analyzer, dic, destinationdic, connection, capacity)
    return analyzer

def addCountry(analyzer, dic):
    if dic["CapitalName"] == "":
        return None
    else: 
        capital = dic["CapitalName"] 
        clat = float(dic["CapitalLatitude"])
        clon = float(dic["CapitalLongitude"])
        addLandingPoint(analyzer, capital)
        country = dic["CountryName"].lower().replace(" ", "")
        a = mp.get(analyzer['countries_cables'], country)
        if a == None:
            mind = 10**15
            nlp = ""
            lps = mp.keySet(analyzer['landing_points'])
            for e in lt.iterator(lps):
                b = mp.get(analyzer['landing_points'], e)
                edic = me.getValue(b)
                distance = haversine(clon, clat, edic["longitude"], edic["latitude"])
                if distance < mind:
                    mind = distance
                    nlp = edic["name"].split(",")[0]
            c = mp.get(analyzer['landing_points_cables'], nlp)
            lpvertexs = me.getValue(c)
            lpvertex = lt.getElement(lpvertexs, 0)
            addCable(analyzer, capital, lpvertex, mind)
            addCable(analyzer, lpvertex, capital, mind)
            connection = capital + "-" + lpvertex + "-" + "CC"
            addCapacity(analyzer, connection, 12.8) 
        else:
            clist = me.getValue(a)
            for i in lt.iterator(clist):
                distance = haversine(clon, clat, i["longitude"], i["latitude"])
                addCable(analyzer, capital, i["vertex"], distance)
                addCable(analyzer, i["vertex"], capital, distance)
                connection = capital + "-" + i["vertex"] + "-" + "CC"
                addCapacity(analyzer, connection, i["mincapacity"])
        mp.put(analyzer["countries"], dic["CountryName"].lower().replace(" ", ""), dic)
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
    lpname = lpinfo["name"]
    name = lpname + '-' + cable
    addVertexLandingPoint(analyzer, lpname, name)
    return name

def addVertexLandingPoint(analyzer, lp, name):
    lpname = lp.split(",")[0]
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

def addCountryLandingPoint(analyzer, landingpoint, lpvertexdic, connection, capacity):
    lpinfo = getLandingPointInfo(analyzer, landingpoint["destination"])
    lpname = lpinfo["name"].split(",")
    lpvertex = lpvertexdic["destination"]
    lat = lpvertexdic["latitude"]
    lon = lpvertexdic["longitude"]
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
    lt.addLast(countrylist, {"name": connection, "capacity": capacity, "vertex": lpvertex,
                                "latitude": lat, "longitude": lon, "mincapacity": 0})

    min = 10**15
    for i in lt.iterator(countrylist):
        if i["capacity"] < min:
            min = i["capacity"]

    for i in lt.iterator(countrylist):         
        if i["vertex"] != lpvertex:
            addCable(analyzer, lpvertex, i["vertex"], 0.1)
            connection = lpvertex + "-" + i["vertex"] + "-" + "IC"
            addCapacity(analyzer, connection, min)
            i["mincapacity"] = min

    mp.put(analyzer['countries_cables'], country, countrylist)

    return analyzer

# Funciones de consulta
def totalVertexs(analyzer):
    return gr.numVertices(analyzer['cables'])

def totalConnections(analyzer):
    return gr.numEdges(analyzer['cables'])

def totalCountries(analyzer):
    return mp.size(analyzer['countries'])

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def clustersandlandingpoints(analyzer, lp1, lp2):
    analyzer['components'] = scc.KosarajuSCC(analyzer['cables'])
    clusters = scc.connectedComponents(analyzer['components'])
    a = mp.get(analyzer["landing_points_cables"], lp1)
    lp1list = me.getValue(a)
    b = mp.get(analyzer["landing_points_cables"], lp2)
    lp2list = me.getValue(b)

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
        namelist = lpinfo["name"].split(",")
        dic["name"] = namelist[0]
        if len(namelist) == 3:
            dic["country"] = namelist[2]
        if len(namelist) == 2:
            dic["country"] = namelist[1]
        else:
            dic["country"] = namelist[0]
        b = mp.get(analyzer["landing_points_cables"], dic["name"])
        lplist = me.getValue(b)
        if lt.size(lplist) > 1:
            dic["total"] = str(lt.size(lplist))
            lt.addLast(lpslist, dic)

    return lpslist

def minroute(analyzer, p1, p2):
    a = mp.get(analyzer["countries"], p1)
    cap1 = me.getValue(a)["CapitalName"]
    b = mp.get(analyzer["countries"], p2)
    cap2 = me.getValue(b)["CapitalName"]
    analyzer['paths'] = djk.Dijkstra(analyzer['cables'], cap1)
    path = djk.pathTo(analyzer['paths'], cap2)
    totdis = 0
    for i in lt.iterator(path):
        totdis+= i["weight"]
    return (path, totdis)

def criticalstructure(analyzer):
    analyzer["prim"] = pr.PrimMST(analyzer["cables"])
    vlist = gr.vertices(analyzer["cables"])
    randomvertex = lt.getElement(vlist, randint(0, lt.size(vlist)))
    mst = pr.prim(analyzer["cables"], analyzer["prim"], randomvertex)
    weight = pr.weightMST(analyzer["cables"], analyzer["prim"])
    nlps = 0
    totvertex = mp.keySet(mst["marked"])
    for i in lt.iterator(totvertex):
        a = mp.get(mst["marked"], i)
        value = me.getValue(a)
        if value == True:
            nlps+=1
    return (nlps, weight) 

def lpdamage(analyzer, lp):
    a = mp.get(analyzer['landing_points_cables'], lp)
    vertexs = me.getValue(a)
    countries = lt.newList(datastructure= "ARRAY_LIST", cmpfunction= compareValue)
    for i in lt.iterator(vertexs):
        adj = gr.adjacentEdges(analyzer["cables"], i)
        for i in lt.iterator(adj):
            v = ["vertexA", "vertexB"]
            for e in v:
                nm = i[e].split("-")[0]
                name = nm.split(",")
                if len(name) == 3:
                    country = name[2]
                elif len(name) == 2:
                    country = name[1]
                else:
                    country = name[0]
                if lt.isPresent(countries, country) == 0:
                    if i["weight"] != 0.1:
                        lt.addLast(countries, {"country": country, "distance": i["weight"]})

    sort(countries, compareDistance)
    return (countries, lt.size(countries))

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

def compareDistance(lp1, lp2):
    if lp1["distance"] > lp2["distance"]:
        return True
    else:
        return False

# Funciones de ordenamiento
def sort(lst, comparefunction):
    sorted_list = sa.sort(lst, comparefunction)
    return sorted_list
