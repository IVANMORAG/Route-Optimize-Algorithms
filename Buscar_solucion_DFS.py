from flask import Flask, render_template
from Arbol import Nodo

app = Flask(__name__)

# ALGORITMO DE BUSQUEDA EN PROFUNDIDAD

def buscar_solucion_DFS(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)
    
    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop()
        # extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            # solución encontrada
            solucionado = True
            return nodo
        else:
            # expandir nodos hijo
            dato_nodo = nodo.get_datos()
            
            # operador izquierdo
            hijo_izquierdo = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
            if not hijo_izquierdo.en_lista(nodos_visitados) and not hijo_izquierdo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izquierdo)
            
            # operador central
            hijo_central = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
            if not hijo_central.en_lista(nodos_visitados) and not hijo_central.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_central)
            
            # operador derecho
            hijo_derecho = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
            if not hijo_derecho.en_lista(nodos_visitados) and not hijo_derecho.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_derecho)
            
            nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

@app.route('/')
def index():
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    nodo_solucion = buscar_solucion_DFS(estado_inicial, solucion)

    # Procesar los resultados para pasarlo a la plantilla HTML
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()

    return render_template('buscar_solucion_DFS.html', estados=resultado)

if __name__ == '__main__':
    app.run(debug=True)