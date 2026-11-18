import heapq
import math
from collections import Counter

# ============================================================
# 1. DATOS DEL PROBLEMA (Red Eléctrica Urbana)
# ============================================================
nodos = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
coords = {
    'S1': (0, 4), 'S2': (-2, 2), 'S3': (2, 2),
    'S4': (-3, 0), 'S5': (-1, 0), 'S6': (1, 0), 'S7': (3, 0)
}
aristas = [
    ('S4', 'S5', 20), ('S3', 'S6', 30), ('S2', 'S3', 40),
    ('S1', 'S3', 50), ('S2', 'S4', 60), ('S1', 'S2', 70),
    ('S3', 'S7', 80), ('S2', 'S5', 90), ('S6', 'S7', 100),
    ('S5', 'S6', 110)
]

def obtener_distancia(a, b):
    return math.hypot(coords[a][0] - coords[b][0], coords[a][1] - coords[b][1])

# ============================================================
# 2. DIVIDE Y VENCERÁS (Merge Sort para Kruskal)
# ============================================================
def merge_sort_aristas(lista):
    if len(lista) <= 1: return lista
    medio = len(lista) // 2
    izq = merge_sort_aristas(lista[:medio])
    der = merge_sort_aristas(lista[medio:])
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i][2] <= der[j][2]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:]); resultado.extend(der[j:])
    return resultado

# ============================================================
# 3. ALGORITMOS VORACES (Prim y Kruskal)
# ============================================================
def prim(grafo, inicio):
    visitados = set([inicio])
    cola = [(peso, v, inicio) for peso, v in grafo[inicio]]
    heapq.heapify(cola)
    mst, costo = [], 0
    while cola:
        peso, v, u = heapq.heappop(cola)
        if v not in visitados:
            visitados.add(v)
            mst.append((u, v, peso))
            costo += peso
            for sig_peso, sig_nodo in grafo[v]:
                if sig_nodo not in visitados:
                    heapq.heappush(cola, (sig_peso, sig_nodo, v))
    return mst, costo

def kruskal(nodos, aristas):
    padre = {nodo: nodo for nodo in nodos}
    def encontrar(nodo):
        if padre[nodo] == nodo: return nodo
        padre[nodo] = encontrar(padre[nodo])
        return padre[nodo]
    def unir(u, v):
        r, s = encontrar(u), encontrar(v)
        if r != s: padre[r] = s; return True
        return False
    
    aristas_ord = merge_sort_aristas(aristas) # Usa Divide y Vencerás
    mst, costo = [], 0
    for u, v, peso in aristas_ord:
        if unir(u, v):
            mst.append((u, v, peso))
            costo += peso
    return mst, costo

# ============================================================
# 4. PROGRAMACIÓN DINÁMICA (Mochila 0/1)
# ============================================================
def mochila_dp(capacidad_max, herramientas):
    n = len(herramientas)
    dp = [[0 for _ in range(capacidad_max + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        peso, valor = herramientas[i-1]
        for w in range(capacidad_max + 1):
            if peso <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-peso] + valor)
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacidad_max]

# ============================================================
# 5. BACKTRACKING CON PODA (Ruta del Técnico - TSP)
# ============================================================
def ruta_voraz(inicio, nodos_restantes):
    ruta, actual, dist_total = [inicio], inicio, 0
    no_visitados = set(nodos_restantes)
    while no_visitados:
        sig = min(no_visitados, key=lambda n: obtener_distancia(actual, n))
        dist_total += obtener_distancia(actual, sig)
        ruta.append(sig); no_visitados.remove(sig); actual = sig
    dist_total += obtener_distancia(actual, inicio)
    ruta.append(inicio)
    return ruta, dist_total

def backtracking_tsp(nodos, inicio):
    _, limite_voraz = ruta_voraz(inicio, nodos[1:])
    mejor_ruta, mejor_costo, nodos_explorados = [], [limite_voraz], [0]
    
    def _backtrack(actual, ruta_actual, costo_actual, visitados):
        nodos_explorados[0] += 1
        if len(visitados) == len(nodos):
            costo_total = costo_actual + obtener_distancia(actual, inicio)
            if costo_total < mejor_costo[0]:
                mejor_costo[0] = costo_total
                mejor_ruta.clear()
                mejor_ruta.extend(ruta_actual + [inicio])
            return
        for vecino in nodos:
            if vecino not in visitados:
                nueva_dist = costo_actual + obtener_distancia(actual, vecino)
                if nueva_dist < mejor_costo[0]: # FUNCIÓN DE PODA
                    visitados.add(vecino); ruta_actual.append(vecino)
                    _backtrack(vecino, ruta_actual, nueva_dist, visitados)
                    ruta_actual.pop(); visitados.remove(vecino)
                    
    _backtrack(inicio, [inicio], 0, set([inicio]))
    return mejor_ruta, mejor_costo[0], nodos_explorados[0]

# ============================================================
# 6. LCS (Programación Dinámica - Comparar lecturas)
# ============================================================
def lcs(sec1, sec2):
    m, n = len(sec1), len(sec2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if sec1[i-1] == sec2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# ============================================================
# 7. HUFFMAN (Compresión de telemetría)
# ============================================================
def huffman(texto):
    frec = Counter(texto)
    heap = [[peso, [simbolo, ""]] for simbolo, peso in frec.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for par in lo[1:]: par[1] = '0' + par[1]
        for par in hi[1:]: par[1] = '1' + par[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# ============================================================
# EJECUCIÓN Y PRUEBAS
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print(" SMART GRID - MOTOR DE ALGORITMOS")
    print("="*60)
    
    # Preparar grafo
    grafo = {nodo: [] for nodo in nodos}
    for u, v, p in aristas:
        grafo[u].append((p, v)); grafo[v].append((p, u))

    # 1. Voraces
    print("\n[1] PLANIFICACIÓN (Prim y Kruskal)")
    _, c_prim = prim(grafo, 'S1')
    _, c_kruskal = kruskal(nodos, aristas)
    print(f"    Costo MST Prim: {c_prim} m")
    print(f"    Costo MST Kruskal: {c_kruskal} m")
    
    # 2. Mochila
    print("\n[2] MANTENIMIENTO - MOCHILA (Capacidad 50kg)")
    herramientas = [(10, 60), (20, 100), (30, 120), (5, 30)]
    print(f"    Utilidad máxima: {mochila_dp(50, herramientas)}")
    
    # 3. Backtracking
    print("\n[3] MANTENIMIENTO - RUTA (Backtracking)")
    ruta, costo, explorados = backtracking_tsp(nodos, 'S1')
    print(f"    Ruta óptima: {' -> '.join(ruta)}")
    print(f"    Costo: {costo:.2f} m | Nodos explorados: {explorados}")
    
    # 4. LCS
    print("\n[4] TELEMETRÍA - LCS (Datos)")
    s1, s2 = [10, 12, 15, 14, 13], [10, 12, 20, 14, 13, 16]
    print(f"    Lecturas A: {s1}")
    print(f"    Lecturas B: {s2}")
    print(f"    Longitud del patrón común: {lcs(s1, s2)}")
    
    # 5. Huffman
    print("\n[5] TELEMETRÍA - HUFFMAN (Compresión)")
    texto = "ALERTA EN S3"
    codigos = huffman(texto)
    print(f"    Texto original: '{texto}'")
    print(f"    Códigos generados (primeros 3): {codigos[:3]}")