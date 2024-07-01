from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import folium
import math
import os

app = Flask(__name__)

API_KEY = "AIzaSyDytpSLPygjIvXWahgD6BABOeMx6VUTQqU"

ESTADOS = {
    "Mexico": [19.496873, -99.723267],
    "Hidalgo": [20.0910963, -98.7623874],
    "Aguascalientes": [21.8852562, -102.2915677], 
    "Baja California": [30.8406338, -115.2837585],
    "Jalisco": [20.6595382, -103.3494376], 
    "Michoacan": [19.5665192, -101.7068294], 
    "Morelos": [18.6813049, -99.1013498], 
    "Chihuahua": [28.6433753, -106.0587908], 
    "CDMX": [19.4326077, -99.133208], 
    "Nayarit": [21.7513844, -104.8454619], 
    "Guanajuato": [21.0190145, -101.2573586],
    "Guerrero": [17.4391926, -99.54509739999999], 
    "Durango": [24.0248409, -104.6608131],
    "Nuevo Leon": [25.592172, -99.99619469999999], 
    "Campeche": [19.8301251, -90.5349087],
    "Colima": [19.2452342, -103.7240868],
    "Baja California Sur": [26.0444446, -111.6660725],
    "Puebla": [19.0414398, -98.2062727], 
    "Queretaro": [20.5887932, -100.3898881], 
    "Oaxaca": [17.0731842, -96.7265889], 
    "Chiapas": [16.7569318, -93.12923529999999],
    "Quintana Roo": [19.1817393, -88.4791376], 
    "Sinaloa": [25.8226854, -108.2216704], 
    "Yucatan": [20.7098786, -89.0943377],
    "Tlaxcala": [19.318154, -98.2374954],
    "Veracruz": [19.173773, -96.1342241], 
    "Tabasco": [17.8409173, -92.6189273], 
    "Tamaulipas": [24.26694, -98.8362755], 
    "Sonora": [29.2972247, -110.3308814], 
    "Zacatecas": [22.7727913, -102.5765714], 
    "Coahuila": [27.058676, -101.7068294], 
    "San Luis Potosi": [22.1520892, -100.9733024], 
    "Tijuana": [32.5149469, -117.0382471]
}

def obtener_ruta(partida, destino, api_key):
    origin = partida.replace(" ", "+")
    destination = destino.replace(" ", "+")
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK" and "routes" in data and len(data["routes"]) > 0:
        route = data["routes"][0]["legs"][0]
        ruta_nombres = [step["html_instructions"] for step in route["steps"]]
        ruta = " → ".join(ruta_nombres)
        distancia = route["distance"]["text"]
        distancia_valor = route["distance"]["value"] / 1000

        ciudades_por_pasar = [step["start_location"] for step in route["steps"]]
        ciudades_por_pasar.append(route["steps"][-1]["end_location"])

        return ruta, distancia, distancia_valor, data, ciudades_por_pasar
    else:
        return None, None, None, None, None

def obtener_coordenadas(data):
    coordenadas = []
    for step in data["routes"][0]["legs"][0]["steps"]:
        lat, lng = step["start_location"]["lat"], step["start_location"]["lng"]
        coordenadas.append((lat, lng))
    lat, lng = data["routes"][0]["legs"][0]["steps"][-1]["end_location"]["lat"], data["routes"][0]["legs"][0]["steps"][-1]["end_location"]["lng"]
    coordenadas.append((lat, lng))
    return coordenadas

def dibujar_ruta_en_mapa(partida, destino, coordenadas):
    mapa = folium.Map(location=coordenadas[0], zoom_start=10)
    folium.Marker(coordenadas[0], popup="Inicio", icon=folium.Icon(color='red')).add_to(mapa)
    folium.Marker(coordenadas[-1], popup="Destino", icon=folium.Icon(color='green')).add_to(mapa)
    folium.PolyLine(locations=coordenadas, color='blue').add_to(mapa)
    ruta_html_path = os.path.join("static", "ruta_interactiva.html")
    mapa.save(ruta_html_path)
    print("Se ha creado un archivo 'ruta_interactiva.html' con el mapa interactivo.")

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos
    utilizando la fórmula del haversine.
    """
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia de latitud y longitud
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Aplicar la fórmula del haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calcular la distancia
    distancia = R * c

    return distancia

def encontrar_ciudades_por_pasar(coordenadas):
    ciudades = []
    for lat, lng in coordenadas:
        ciudad_cercana = None
        menor_distancia = float('inf')
        for estado, (lat_estado, lng_estado) in ESTADOS.items():
            distancia = calcular_distancia(lat_estado, lng_estado, lat, lng)
            if distancia < menor_distancia:
                menor_distancia = distancia
                ciudad_cercana = estado
        if ciudad_cercana:
            ciudades.append(ciudad_cercana)
    return list(dict.fromkeys(ciudades))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta', methods=['POST'])
def calcular_ruta():
    data = request.json
    partida = data['partida']
    destino = data['destino']

    print("Partida:", partida)
    print("Destino:", destino)

    ruta, distancia, distancia_valor, datos_ruta, ciudades_por_pasar = obtener_ruta(partida, destino, API_KEY)

    if ruta is not None:
        coordenadas = obtener_coordenadas(datos_ruta)
        dibujar_ruta_en_mapa(partida, destino, coordenadas)

        ciudades_nombres = encontrar_ciudades_por_pasar(coordenadas)

        return jsonify({
            'ruta': ruta,
            'distancia': distancia,
            'ciudades_por_pasar': ciudades_nombres
        })
    else:
        return jsonify({'error': 'No se encontró una ruta válida para los destinos seleccionados.'}), 400

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)