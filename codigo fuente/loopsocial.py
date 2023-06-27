import networkx as nx
import heapq as hq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import copy
import operator

# Crear el grafo
G = nx.DiGraph()


#crear dataframes de los archivos csv
usuarios = pd.read_csv('D:\\Users\\carlo\\Desktop\\complejidad\\TF\\FINAL\\usuariosBD.csv')
conexiones = pd.read_csv('D:\\Users\\carlo\\Desktop\\complejidad\\TF\\FINAL\\conexionesDataSetPRUEBA.csv')

#convertir el dataframe en una lista
userlist = usuarios.to_numpy().tolist() # Lista de usuarios 
cnxslist = conexiones.to_numpy().tolist() # Lista de conexiones


def buscar(nombre):
    for i in range(len(userlist)):
        if nombre == userlist[i][0]:
            return i

def calcularpeso(nodo1, nodo2):
    peso = 1
    for i in range(11):
        #print(i)
        if userlist[nodo1][2+i] == userlist[nodo2][2+i] == 1:
            peso += 2
    return peso

pesos = []
iterador = 0
for i in range(len(userlist)):
    listaaux = []
    while userlist[i][0] == cnxslist[iterador][0]:        
        destino = buscar(cnxslist[iterador][1])
        peso = calcularpeso(i,destino)
        listaaux.append((destino,peso))
        iterador += 1
        if iterador >= len(cnxslist):
            break
    pesos.append(listaaux)
#print(pesos) # [[(6, 5), (1, 3), (8, 1)], [(2, 5), (3, 5), (4, 3)], [(5, 5), (8, 5)], [(4, 1)]]

def lstGrafo(G,lista):
    aux = copy.deepcopy(cnxslist)
    var = 0
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            aux[var].append(lista[i][j][1])
            var += 1
    for edge in aux:
        node1, node2, weight = edge
        G.add_edge(node1, node2, weight=weight)
    return G

def lstGrafoNum(G,lista):
    for i in range(len(lista)):
        for j in range(len(lista[i])):
            weight = lista[i][j][1]
            G.add_edge(i, lista[i][j][0], weight=weight)
    return G

def lstGrafoId(G,lista,indice):

    aux = copy.deepcopy(cnxslist)
    var = 0
    final = []

    for i in range(len(lista)):
        for j in range(len(lista[i])):
            id = indice[i]
            origen = userlist[id][0]
            iddestino = lista[i][j][0]
            destino = userlist[iddestino][0]
            peso = lista[i][j][1]
            final.append([origen,destino,peso])

    for edge in final:
        
        node1, node2, weight = edge
        G.add_edge(node1, node2, weight=weight)
    return G

def lstGrafoIdNum(G,lista,indice):
    aux = copy.deepcopy(cnxslist)
    var = 0
    final = []

    for i in range(len(lista)):
        for j in range(len(lista[i])):
            origen = indice[i]
            destino = lista[i][j][0]
            peso = lista[i][j][1]
            G.add_edge(origen, destino, weight=peso)
    return G

def traductor(lista,indices):
    final = copy.deepcopy(lista)
    for z in range(len(indices)):
        aux = []
        for i in range(len(lista)):       
            for j in range(len(lista[i])):
                if lista[i][j][0] == indices[z]:
                    final[i][j] = (z,lista[i][j][1])

    return final


G = lstGrafoNum(G,pesos)



def dijkstra(G, s, res):
    n = len(G)
    visited = [False]*n
    path = [-1]*n
    cost = [-math.inf]*n

    cost[s] = 0
    pqueue = [(0, s)]
    visited_count = 0
    while pqueue and visited_count < res:
        g, u = hq.heappop(pqueue)
        if not visited[u]:
            visited[u] = True
            visited_count += 1
            for v, w in G[u]:
                if not visited[v]:
                    f = g + w
                    if f > cost[v]:
                        cost[v] = f
                        path[v] = u
                        hq.heappush(pqueue, (f, v))
            
                            
    return path, cost

def amigosDeAmigos(nodoInicial):
    amigos = [] 
    aux1 = pesos[nodoInicial]

    indices = [nodoInicial]

    amigos.append(aux1)
    aux = []
    for i in range(len(aux1)):
        var = pesos[nodoInicial][i][0]
        aux = pesos[var]
        amigos.append(aux)

        indices.append(var)

    return amigos, indices


listaAmigos, listaIndices = amigosDeAmigos(4)

G2 = nx.DiGraph()
#G2 = lstGrafoId(G2, listaAmigos,listaIndices)
G2 = lstGrafoIdNum(G2, listaAmigos, listaIndices)


def tamanio(matriz):
    total = 0
    for i in range(len(matriz)):
        total += len(matriz[i])
    return total

restriccion = tamanio(listaAmigos)

path, cost = dijkstra(pesos, 4,restriccion)
print(path)
print(cost)

pos = nx.layout.shell_layout(G)
nx.draw_networkx(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edges(G2, pos, edge_color='r', width=2)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.show()
