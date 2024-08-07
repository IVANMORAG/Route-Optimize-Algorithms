# Route Optimize Algorithms

Este repositorio contiene implementaciones de algoritmos para la optimización de rutas y búsqueda. El propósito principal es encontrar la ruta más corta entre ciudades utilizando coordenadas en formato JSON. Los algoritmos y ejercicios incluidos son:

- **BFS (Breadth-First Search)**: Algoritmo de búsqueda en anchura.
- **DFS (Depth-First Search)**: Algoritmo de búsqueda en profundidad.
- **Dijkstra**: Algoritmo para encontrar el camino más corto en un grafo.
- **Simulated Annealing**: Algoritmo de optimización basado en el enfriamiento simulado.
- **Hill Climbing**: Algoritmo de búsqueda que iterativamente mejora la solución.

Cada algoritmo está acompañado de su respectivo archivo HTML y CSS para la visualización de resultados.

## Estructura del Repositorio

El repositorio está organizado en los siguientes archivos y carpetas:

- `static/`: Archivos estáticos necesarios para la aplicación.
- `templates/`: Plantillas para la interfaz de usuario.
- `Arbol.py`: Implementación del algoritmo de búsqueda en árbol.
- `Buscar_solucion_BFS.py`: Implementación del algoritmo BFS.
- `Buscar_solucion_DFS.py`: Implementación del algoritmo DFS.
- `DFS_prof_iter.py`: Implementación del algoritmo DFS iterativo.
- `Dijkstra.py`: Implementación del algoritmo de Dijkstra.
- `Hill_Climbling.py`: Implementación del algoritmo de Hill Climbing.
- `Hill_climbing_iterativo.py`: Implementación del algoritmo de Hill Climbing iterativo.
- `Simulated_annealing.py`: Implementación del algoritmo de Simulated Annealing.
- `app.py`: Archivo principal de la aplicación.
- `puzzleLineal.py`: Implementación del algoritmo BFS para resolver el problema de puzzle lineal.

## Requisitos

Asegúrate de tener instalados los siguientes paquetes para ejecutar el proyecto:

- Flask
- requests
- folium
- math (incluido en la biblioteca estándar de Python)
- os (incluido en la biblioteca estándar de Python)

Puedes instalar las dependencias necesarias utilizando pip:

```bash
pip install Flask requests folium
```

## Uso

Para ejecutar un algoritmo específico, utiliza el archivo Python correspondiente. Por ejemplo:

```bash
python Buscar_solucion_BFS.py
```

## Información adicional

API_KEY: Se utiliza una clave de API para algunas funcionalidades. Asegúrate de configurarla en el archivo app.py.

```
API_KEY = "AIzaSyDytpSLPygjIvXWahgD6BABOeMx6VUTQqU"
```
