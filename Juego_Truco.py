"""Valores de las cartas"""

"""Función para envido"""
def calcular_envido(mano):
    puntos = 0
    palos_dict = {}

    for carta in mano:
        valor = carta[0]
        palo = carta[1]

        if valor <= 7:
            if palo not in palos_dict:
                palos_dict[palo] = []
            palos_dict[palo].append(valor)

    for palo in palos_dict:
        if len(palos_dict[palo]) >= 2:
            puntos = max(puntos, palos_dict[palo][0] + palos_dict[palo][1] + 20)

    return puntos

def decidir_envido(mano):
    return calcular_envido(mano) > 24

"""Función para el truco"""
def decidir_truco(mano):
    for carta in mano:
        if carta[0] > 2:
            return True
    return False

def decidir_retruco(mano):
    for carta in mano:
        if carta[0] == 7 and (carta[1] == "espada" or carta[1] == "oro"):
            return True
    return False

def decidir_valecuatro(mano):
    for carta in mano:
        if carta[0] == 1 and (carta[1] == "espada" or carta[1] == "basto"):
            return True
    return False

"""Puntos para el envido"""
def resultado_envido(gana_pc, rechazado, puntos_juego, marcador):
    if rechazado:
        marcador["pc"] += 1
    else:
        if gana_pc:
            marcador["pc"] += 2
        else:
            marcador["jugador"] += 2
            
"""Puntos para el truco"""
def resultado_truco(nivel, ganado_pc, rechazado, marcador):
    if rechazado:
        marcador["pc"] += 1
        return

    if nivel == 1:  #truco
        puntos = 2
    elif nivel == 2:  #retruco
        puntos = 3
    else:  #valecuatro
        puntos = 4

    if ganado_pc:
        marcador["pc"] += puntos
    else:
        marcador["jugador"] += puntos
        
"""Puntos por ronda sin truco y sin envido"""
def resultado_ronda(gana_pc, marcador):
    if gana_pc:
        marcador["pc"] += 1
    else:
        marcador["jugador"] += 1
        
"""Definición de ganador"""
def hay_ganador(marcador, limite):
    if marcador["pc"] >= limite:
        return "PC"
    elif marcador["jugador"] >= limite:
        return "Jugador"
    return None

#Programa Principal
marcador = {"pc": 0, "jugador": 0}
limite = 15 #modificar y poner en opción si es 15 o 30

"""modificarlo en base a como se creara el mazo"""
mazo = crear_mazo()
mezclar_mazo(mazo)

mano_pc, mano_jugador = repartir(mazo)

print("Mano PC:", mano_pc)

"""Decisiones de la compu"""
if decidir_envido(mano_pc):
    print("PC canta Envido")

if decidir_truco(mano_pc):
    print("PC canta Truco")

if decidir_retruco(mano_pc):
    print("PC canta Retruco")

if decidir_valecuatro(mano_pc):
    print("PC canta Vale Cuatro")