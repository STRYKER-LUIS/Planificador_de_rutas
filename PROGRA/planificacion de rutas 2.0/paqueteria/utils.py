import math
from typing import Dict, List, Tuple, Set

class Grafo:
    def __init__(self):
        self.vertices: Dict[str, Dict[str, float]] = {}
        self.coordenadas: Dict[str, Tuple[float, float]] = {}

    def agregar_vertice(self, id: str, lat: float, lon: float):
        if id not in self.vertices:
            self.vertices[id] = {}
            self.coordenadas[id] = (lat, lon)

    def agregar_arista(self, origen: str, destino: str, peso: float):
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen][destino] = peso
            # Agregar arista en ambas direcciones para un grafo no dirigido
            self.vertices[destino][origen] = peso

    def calcular_distancia(self, punto1: Tuple[float, float], punto2: Tuple[float, float]) -> float:
        """Calcula la distancia entre dos puntos usando la fórmula de Haversine"""
        lat1, lon1 = punto1
        lat2, lon2 = punto2
        
        # Radio de la Tierra en kilómetros
        R = 6371.0
        
        # Convertir grados a radianes
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Diferencia de coordenadas
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        # Fórmula de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distancia = R * c
        
        return distancia

    def encontrar_punto_cercano(self, punto: Tuple[float, float], radio_maximo: float = 5.0) -> str:
        """Encuentra el punto más cercano en el grafo dentro de un radio máximo"""
        punto_cercano = None
        distancia_minima = float('inf')
        
        for id, coords in self.coordenadas.items():
            distancia = self.calcular_distancia(punto, coords)
            if distancia < distancia_minima and distancia <= radio_maximo:
                distancia_minima = distancia
                punto_cercano = id
        
        return punto_cercano

    def dijkstra(self, inicio: str, fin: str) -> Tuple[List[str], float]:
        """Implementa el algoritmo de Dijkstra para encontrar la ruta más corta"""
        if inicio not in self.vertices or fin not in self.vertices:
            return [], float('inf')

        # Inicialización
        distancias = {v: float('inf') for v in self.vertices}
        distancias[inicio] = 0
        predecesores = {v: None for v in self.vertices}
        no_visitados = set(self.vertices.keys())

        while no_visitados:
            # Encontrar el vértice no visitado con la distancia mínima
            actual = min(no_visitados, key=lambda v: distancias[v])
            
            if actual == fin:
                break

            no_visitados.remove(actual)

            # Actualizar distancias a los vecinos
            for vecino, peso in self.vertices[actual].items():
                if vecino in no_visitados:
                    nueva_distancia = distancias[actual] + peso
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        predecesores[vecino] = actual

        # Reconstruir la ruta
        ruta = []
        actual = fin
        while actual is not None:
            ruta.append(actual)
            actual = predecesores[actual]
        ruta.reverse()

        return ruta, distancias[fin]

    def obtener_coordenadas_ruta(self, ruta: List[str]) -> List[Tuple[float, float]]:
        """Convierte una lista de IDs de vértices en una lista de coordenadas"""
        return [self.coordenadas[v] for v in ruta]

def crear_grafo_guatemala() -> Grafo:
    """Crea un grafo con puntos importantes de Guatemala"""
    grafo = Grafo()
    
    # Agregar puntos importantes de Guatemala
    puntos = {
        'ciudad_guatemala': (14.6349, -90.5069),
        'mixco': (14.6333, -90.6064),
        'villa_nueva': (14.5269, -90.5875),
        'petapa': (14.5019, -90.5619),
        'chinautla': (14.7033, -90.4997),
        'san_juan_sacatepequez': (14.7189, -90.6444),
        'villa_canales': (14.4472, -90.5317),
        'san_miguel_petapa': (14.5019, -90.5619),
        'amatitlan': (14.4775, -90.6344),
        'san_jose_pinula': (14.5461, -90.4114)
    }

    # Agregar vértices
    for id, coords in puntos.items():
        grafo.agregar_vertice(id, coords[0], coords[1])

    # Agregar aristas (conexiones entre puntos)
    for origen in puntos:
        for destino in puntos:
            if origen != destino:
                distancia = grafo.calcular_distancia(puntos[origen], puntos[destino])
                # Solo agregar conexiones si están dentro de un radio razonable
                if distancia <= 10.0:  # 10 km máximo
                    grafo.agregar_arista(origen, destino, distancia)

    return grafo 