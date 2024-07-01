from flask import Flask, render_template
from Arbol import Nodo

app = Flask(__name__)

# ALGORTMO DE BUSQUEDA EN PROFUNDIDAD BFS

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera[0]
        # extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))

        if nodo.get_datos() == solucion:
            # solución encontrada
            solucionado = True
            return nodo
        else:
            # expandir nodos hijo (ciudades con conexión)
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)

@app.route('/')
def index():
    conexiones = {
        'CDMX': ['SLP', 'MEXICALI', 'CHIHUAHUA'],
        'ZAPOPAN': ['ZACATECAS', 'MEXICALI'],
        'GUADALAJARA': ['CHIAPAS'],
        'CHIAPAS': ['CHIHUAHUA'],
        'MEXICALI': ['SLP', 'ZAPOPAN', 'CDMX', 'CHIHUAHUA', 'SONORA'],
        'SLP': ['CDMX', 'MEXICALI'],
        'ZACATECAS': ['ZAPOPAN', 'SONORA', 'CHIHUAHUA'],
        'SONORA': ['ZACATECAS', 'MEXICALI'],
        'MICHOACAN': ['CHIHUAHUA'],
        'CHIHUAHUA': ['MICHOACAN', 'ZACATECAS', 'MEXICALI', 'CDMX', 'CHIAPAS']
    }

    estado_inicial = 'CDMX'
    solucion = 'ZACATECAS'

    nodo_solucion = buscar_solucion_BFS(conexiones, estado_inicial, solucion)

    # mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    
    return render_template('buscar_solucion_BFS.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)