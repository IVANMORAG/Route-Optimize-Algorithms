from flask import Flask, render_template
from Arbol import Nodo

app = Flask(__name__)

#ALGORITMO DE BUSQUEDA EN PROFUNDIDAD ITERATIVA

def DFS_prof_iter(nodo, solucion, conexiones):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite, conexiones)
        if sol != None:
            return sol

def buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite, conexiones):
    if limite > 0:
        visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                if not hijo.en_lista(visitados):
                    lista_hijos.append(hijo)

            nodo.set_hijos(lista_hijos)

            for nodo_hijo in nodo.get_hijos():
                if nodo_hijo.get_datos() not in visitados:
                    sol = buscar_solucion_DFS_Rec(nodo_hijo, solucion, visitados, limite-1, conexiones)
                    if sol != None:
                        return sol
                    
        return None

@app.route('/')
def buscar_ruta():
    conexiones = {
        'EDO.MEX': {'QRO', 'SLP', 'SONORA'},
        'PUEBLA': {'HIDALGO', 'SLP'},
        'CDMX': {'MICHOACAN'},
        'MICHOACAN': {'SONORA'},
        'SLP': {'QRO', 'PUEBLA', 'EDO.MEX', 'SONORA', 'GUADALAJARA'},
        'QRO': {'EDO.MEX', 'SLP'},
        'HIDALGO': {'PUEBLA', 'GUADALAJARA', 'SONORA'},
        'GUADALAJARA': {'HIDALGO', 'SLP'},
        'MONTERREY': {'SONORA'}, 
        'SONORA': {'MONTERREY', 'HIDALGO', 'SLP', 'EDO.MEX', 'MICHOACAN'}
    }
    estado_inicial = 'EDO.MEX'
    solucion = 'HIDALGO'
    nodo_inicial = Nodo(estado_inicial)
    nodo = DFS_prof_iter(nodo_inicial, solucion, conexiones)
    if nodo != None:
        resultado = []
        while nodo.get_padre() != None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        return render_template('DFS_prof_iter.html', resultado=resultado)
    else:
        return render_template('DFS_prof_iter.html', mensaje="Solución no Encontrada")

if __name__ == "__main__":
    app.run(debug=True)



    ruta = i_hill_climbing()
    print(ruta)
    print("Distancia Total:", evalua_ruta(ruta))