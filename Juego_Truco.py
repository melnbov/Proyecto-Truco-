
import random
palos = ["oro", "copa", "espada", "basto"]
numeros = [1,2,3,4,5,6,7,10,11,12]

valores_cartas={
    (1, "espada"): 14,
    (1, "basto"): 13,
    (7, "espada"): 12,
    (7, "oro"): 11,
    3: 10,
    2: 9,
    1: 8,
    12: 7,
    11: 6,
    10: 5,
    7: 4,
    6: 3,
    5: 2,
    4: 1
}
    

def valor_truco(numero,palo):
   return valores_cartas.get((numero,palo), valores_cartas[numero])

def crear_mazo():
    """
    Crea el mazo de cartas del Truco argentino.
    Cada carta es una lista: [numero, palo, valor_truco]
    Retorna el mazo completo sin mezclar.
    """
    mazo = []
    for palo in palos:
        for numero in numeros:
            mazo.append([numero, palo, valor_truco(numero,palo)])
    return mazo

def mezclar_mazo(mazo):
    """
    Mezcla aleatoriamente el mazo usando random.shuffle.
    Modifica el mazo original.
    """
    random.shuffle(mazo)

def repartir(mazo):
    """
    Reparte 3 cartas a la PC y 3 al jugador.
    Retorna dos listas: mano_pc y mano_jugador.
    """
    mano_pc = mazo[:3]
    mano_jugador = mazo[3:6]
    return mano_pc, mano_jugador
    
"""Valores de las cartas"""

"""Función para envido"""
def calcular_envido(mano):
    """
    La función "calcular_envido" recibe una mano de cartas y calcula
    el puntaje de envido del jugador o la computadora.
    Solo se toman en cuenta las cartas del 1 al 7 y se agrupan por palo.
    Si hay dos cartas del mismo palo, se suman sus valores y se le agregan 20 puntos.
    Retorna el puntaje más alto posible de envido.
    """
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
    """
    La función "decidir_envido" evalúa si la computadora debería cantar envido.
    Utiliza el resultado de calcular_envido y decide cantar solo si
    el puntaje es mayor a 24.
    Retorna True si conviene cantar envido, False en caso contrario.
    """
    return calcular_envido(mano) > 24

"""Función para el truco"""
def decidir_truco(mano):
    """
    La función "decidir_truco" determina si la computadora debe cantar truco.
    Recorre las cartas de la mano y si encuentra alguna con valor mayor a 2,
    decide cantar truco.
    Retorna True si canta truco, False si no.
    """
    return any(carta[2] >= 10 for carta in mano)
    
def decidir_retruco(mano):
    """
    La función "decidir_retruco" determina si la computadora debe cantar retruco.
    Si la mano contiene un 7 de espada o un 7 de oro, decide cantar retruco.
    Retorna True si canta retruco, False en caso contrario.
    """
    for carta in mano:
        if carta[0] == 7 and (carta[1] == "espada" or carta[1] == "oro"):
            return True
    return False

def decidir_valecuatro(mano):
    """
    La función "decidir_valecuatro" determina si la computadora debe cantar vale cuatro.
    Si la mano contiene un 1 de espada o un 1 de basto (las cartas más fuertes),
    decide cantarlo.
    Retorna True si canta vale cuatro, False en caso contrario.
    """
    for carta in mano:
        if carta[0] == 1 and (carta[1] == "espada" or carta[1] == "basto"):
            return True
    return False

"""Puntos para el envido"""
def resultado_envido(gana_pc, rechazado, puntos_juego, marcador):
    """
    La función "resultado_envido" actualiza el marcador según el resultado del envido.
        - Si el envido es rechazado, la computadora gana 1 punto.
        - Si se juega, el ganador suma 2 puntos.
    Parámetros:
        gana_pc: indica si la computadora ganó el envido.
        rechazado: indica si el envido fue rechazado.
        puntos_juego: actualmente no se utiliza.
        marcador: diccionario con los puntos del jugador y la PC.
    """
    if rechazado:
        marcador["pc"] += 1
    else:
        if gana_pc:
            marcador["pc"] += 2
        else:
            marcador["jugador"] += 2
            
"""Puntos para el truco"""
puntos_truco={
    1:2, #truco
    2:3, #retruco
    3:4 #vale cuatro
}

def resultado_truco(nivel, ganado_pc, rechazado, marcador, cantado_por):
    """
    La función "resultado_truco" actualiza el marcador según el resultado del truco.
    Parámetros:
       nivel: nivel de la apuesta (1=truco, 2=retruco, 3=vale cuatro).
       ganado_pc: indica si la computadora ganó la ronda.
       rechazado: indica si el truco fue rechazado.
       marcador: diccionario con los puntos.
       cantado_por: "pc" o "jugador".
    """
    if rechazado:
        # El punto lo gana quien cantó el truco
        marcador[cantado_por] += nivel
        return

    puntos=puntos_truco[nivel]

    if ganado_pc:
        marcador["pc"] += puntos
    else:
        marcador["jugador"] += puntos
        
"""Puntos por ronda sin truco y sin envido"""
def resultado_ronda(gana_pc, marcador):
    """
    La función "resultado_ronda" suma puntos cuando no hubo truco ni envido.
    El ganador de la ronda suma 1 punto.
    Parámetros:
       gana_pc: indica si la computadora ganó la ronda.
       marcador: diccionario con los puntos.
    """
    if gana_pc:
        marcador["pc"] += 1
    else:
        marcador["jugador"] += 1
        
"""Definición de ganador"""
def hay_ganador(marcador, limite):
    """
    La función "hay_ganador" verifica si alguno de los jugadores alcanzó el puntaje límite.
    Si la computadora llega al límite, devuelve "PC".
    Si el jugador llega al límite, devuelve "Jugador".
    Si nadie llegó todavía, devuelve None.
    """
    if marcador["pc"] >= limite:
        return "PC"
    elif marcador["jugador"] >= limite:
        return "Jugador"
    return None

def reglasDeJuego():
    """
    La funcion "reglasDeJuego" tiene 3 opciones en la que se puede ver
    las reglas generales del juego, ver el sistema de puntos, ver 
    reestricciones del juego y salir al menu principal 

    """
    opcion="0"

    while opcion != "4":
        print("\n===== Reglas del Truco =====")
        print("1. Ver reglas generales")
        print("2. Ver sistema de puntos")
        print("3. Ver restricciones")
        print("4. Salir de reglas del truco")
        opcion=input("\nIngresa una opcion: ")

        if opcion not in ["1","2","3","4"]:
            print("Opción invalida. Ingresá un numero del 1 al 4.")
        else:
            if opcion == "1":
                print("\n--- Reglas Generales ---")
                print("- El juego será entre el jugador y la computadora")
                print("- La partida podrá ser hasta 15 o 30 puntos")
                print("- Se va a poder cantar, Envido, Truco, Retruco y Valecuatro")
                print("- Se gana cuando el jugador o la computadora llega a 15 o 30 puntos")

            elif opcion == "2":
                print("\n--- Sistema de Puntos ---")
                print("- Retirarse en la primera ronda: 1 punto al contrincante.")
                print("- Ganar el Envido: 2 puntos.")
                print("- Rechazar el Envido: 1 punto al que lo cantó.")
                print("- Ganar el Truco: 2 puntos.")
                print("- Retruco: 3 puntos.")
                print("- Valecuatro: 4 puntos.")
                print("- Rechazar el Truco: 1 punto al que lo cantó.")
                print("- Sin cantos: 1 punto al ganador de la ronda.")

            elif opcion == "3":
                print("\n--- Restricciones ---")
                print("- No se podrá cantar flor.")
                print("- No hay envido envido, falta envido y real envido.")
            
            elif opcion == "4":
                print("Volviendo al menú principal...")
            

def menuDeInicio():
    """
    La funcion "menuDeInicio" se ejecutara al inicio del juego,
    va a dejar al usuario ingresar a una nueva partida, ver las reglas del juego,
    ver su historial de partidas y salir 
    """
    opcion = "0"

    while opcion != "4":
        print("¡Bienvenidos al Juego del Truco!")
        print("1. Jugar una nueva partida")
        print("2. Ver reglas del juego")
        print("3. Ver historial de jugadas")
        print("4. Salir")

        opcion = input("Ingresa una opcion: ")

        if opcion not in ["1", "2", "3", "4"]:
            print("Opcion inválida. Ingresá un numero del 1 al 4")
        else:
            if opcion == "1":
                print("Iniciando juego...")
                jugar_partida()
            elif opcion == "2":
                reglasDeJuego()
            elif opcion == "3":
                print("Mostrando historial...")
            elif opcion == "4":
                print("¡Hasta Luego!")


def jugar_partida():
    """
    Ejecuta una partida del Truco.
    - Crea y mezcla el mazo
    - Reparte cartas
    - Muestra la mano del jugador
    - Evalúa decisiones automáticas de la PC
    - Espera al usuario para volver al menú
    """
    marcador = {"pc": 0, "jugador": 0}

    mazo = crear_mazo()
    mezclar_mazo(mazo)

    mano_pc, mano_jugador = repartir(mazo)

    print("\n===== INICIANDO PARTIDA =====")

    print("\nMano del Jugador:")
    for c in mano_jugador:
        print(c)

    print("\n===== DECISIONES DE LA PC =====")

    if decidir_envido(mano_pc):
        print("PC canta ENVIDO")

    if decidir_truco(mano_pc):
        print("PC canta TRUCO")

    if decidir_retruco(mano_pc):
        print("PC canta RETRUCO")

    if decidir_valecuatro(mano_pc):
        print("PC canta VALE CUATRO")
    
    input("\nPresioná ENTER para volver al menú...")
    
menuDeInicio()