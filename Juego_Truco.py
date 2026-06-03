import random

PALOS = ["oro", "copa", "espada", "basto"]
NUMEROS = [1,2,3,4,5,6,7,10,11,12]

VALORES_CARTAS = {
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

def valor_truco(numero, palo):
    """
    Devuelve el valor de una carta según las reglas del Truco.
    """
    return VALORES_CARTAS.get((numero,palo), VALORES_CARTAS[numero])

def crear_mazo():
    """
    Crea el mazo completo de Truco.
    Cada carta tiene:
    (numero, palo)
    """
    return{
        (numero,palo)
        for palo in PALOS
        for numero in NUMEROS
    }


def repartir(mazo):
    """
    Reparte 3 cartas a la PC
    y 3 cartas al jugador.
    """
    mano_pc = random.sample(list(mazo), 3)

    restantes = mazo - set(mano_pc)

    mano_jugador = random.sample(list(restantes), 3)

    return mano_pc, mano_jugador

def elegirpuntos():
    """
    Permite elegir si la partida
    será a 15 o 30 puntos.
    """
    while True:

        try:

            puntos = int(input("¿Desea jugar a 15 o 30 puntos?: "))

            if puntos == 15 or puntos == 30:
                return puntos

            print("Error. Ingrese solamente 15 o 30.")

        except ValueError:

            print("Error. Debe ingresar un número.")

def nombre_carta(carta):
    """
    Convierte una carta en texto.
    """
    return str(carta[0]) + " de " + carta[1]

def mostrar_mano(mano_jugador):
    """
    Muestra las cartas del jugador.
    """
    print("\n===== TUS CARTAS =====")

    i = 0

    while i < len(mano_jugador):

        numero, palo = mano_jugador[i]

        print(str(i+1) + ". " + str(numero) + " de " + palo)

        i += 1

def elegir_mano():
    """
    Decide aleatoriamente
    quién empieza.
    """
    if random.randint(1,2) == 1:
        return "jugador"

    return "pc"

def elegir_carta_jugador(mano_jugador):
    """
    Permite elegir una carta
    o irse al mazo.
    """
    seleccion = -1

    while seleccion < 0 or seleccion > len(mano_jugador):

        print("\n0. Irse al mazo")

        i = 0

        while i < len(mano_jugador):

            numero, palo = mano_jugador[i]

            print(str(i+1) + ". " + str(numero) + " de " + palo)

            i += 1

        try:

            seleccion = int(input("Elegí carta: "))

            if seleccion < 0 or seleccion > len(mano_jugador):

                print("Carta inválida.")

        except ValueError:

            print("Ingresá un número.")
            seleccion = -1

    if seleccion == 0:

        return "mazo"

    try:

        carta = mano_jugador.pop(seleccion - 1)
        return carta

    except IndexError:

        print("La carta elegida no existe.")
        return elegir_carta_jugador(mano_jugador)

def elegir_carta_pc(mano_pc, carta_jugador):
    """
    La PC elige la mejor carta posible.
    """
    if carta_jugador == None:

        carta_pc = min(
            mano_pc,
            key=lambda carta: valor_truco(carta[0], carta[1])
        )

    else:

        cartas_que_ganan = list(filter(
            lambda carta:
                valor_truco(carta[0], carta[1]) >
                valor_truco(carta_jugador[0], carta_jugador[1]),
            mano_pc
        ))

        if len(cartas_que_ganan) > 0:

            carta_pc = min(
                cartas_que_ganan,
                key=lambda carta: valor_truco(carta[0], carta[1])
            )

        else:

            carta_pc = min(
                mano_pc,
                key=lambda carta: valor_truco(carta[0], carta[1])
            )

    mano_pc.remove(carta_pc)

    return carta_pc

def ganador_ronda(carta_jugador, carta_pc):
    """
    Determina el ganador
    de la ronda.
    """
    valor_jugador=valor_truco(
        carta_jugador[0],
        carta_jugador[1]
    )

    valor_pc = valor_truco(
        carta_pc[0],
        carta_pc[1]
    )

    if valor_jugador > valor_pc:

        return "jugador"

    elif valor_pc > valor_jugador:

        return "pc"

    return "parda"

def mostrar_resultado_ronda(carta_jugador, carta_pc, ganador):
    """
    Determina el ganador
    de la ronda.
    """
    print("\nJugador jugó:", nombre_carta(carta_jugador))
    print("PC jugó:", nombre_carta(carta_pc))

    if ganador == "jugador":

        print("Ganaste la ronda.")

    elif ganador == "pc":

        print("La PC ganó la ronda.")

    else:

        print("La ronda fue parda.")

def jugar_ronda(mano_jugador, mano_pc, turno):
    """
    Ejecuta una ronda.
    """
    if turno == "jugador":

        carta_jugador = elegir_carta_jugador(mano_jugador)

        if carta_jugador == "mazo":

            return "mazo"

        carta_pc = elegir_carta_pc(mano_pc, carta_jugador)

    else:

        carta_pc = elegir_carta_pc(mano_pc, None)

        print("\nLa PC juega:", nombre_carta(carta_pc))

        carta_jugador = elegir_carta_jugador(mano_jugador)

        if carta_jugador == "mazo":

            return "mazo"

    ganador = ganador_ronda(carta_jugador, carta_pc)

    mostrar_resultado_ronda(carta_jugador, carta_pc, ganador)

    return ganador

def siguiente_turno(ganador, turno_actual):
    """
    Define quién empieza
    la siguiente ronda.
    """
    if ganador == "parda":

        return turno_actual

    return ganador

def ganador_mano_terminada(resultados, mano):
    """
    Determina el ganador
    final de la mano.
    """
    if len(resultados) == 2:

        primera = resultados[0]
        segunda = resultados[1]

        if primera == "parda" and segunda != "parda":

            return segunda

        elif primera != "parda" and segunda == primera:

            return primera

        elif primera != "parda" and segunda == "parda":

            return primera

    elif len(resultados) == 3:

        primera = resultados[0]
        segunda = resultados[1]
        tercera = resultados[2]

        if primera == "parda" and segunda == "parda" and tercera == "parda":

            return mano

        elif primera == "parda" and segunda != "parda":

            return segunda

        elif tercera != "parda":

            return tercera

        return primera

    return None

def calcular_envido(mano):
    """
    Calcula los puntos de envido.
    """

    try:

        puntos = 0

        palos_dict = {}

        for carta in mano:

            numero = carta[0]
            palo = carta[1]

            if numero >= 10:

                valor_envido = 0

            else:

                valor_envido = numero

            if palo not in palos_dict:

                palos_dict[palo] = []

            palos_dict[palo].append(valor_envido)

        for palo in palos_dict:

            valores = palos_dict[palo]

            if len(valores) >= 2:

                valores.sort(reverse=True)

                puntos = max(
                    puntos,
                    valores[0] + valores[1] + 20
                )

        if puntos == 20:

            mayor = 0

            for carta in mano:

                numero = carta[0]

                if numero >= 10:

                    valor = 0

                else:

                    valor = numero

                if valor > mayor:

                    mayor = valor

            puntos = mayor

        return puntos

    except Exception as error:

        print("Error al calcular envido.")
        print("Error:", error)

        return 0

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
    for carta in mano:

        valor = valor_truco(carta[0], carta[1])

        if valor >= 10:

            return True

    return False

def decidir_retruco(mano):
    """
    La función "decidir_retruco" determina si la computadora debe cantar retruco.
    Si la mano contiene un 7 de espada o un 7 de oro, decide cantar retruco.
    Retorna True si canta retruco, False en caso contrario.
    """
    cartas_fuertes = 0

    for carta in mano:

        valor = valor_truco(carta[0], carta[1])

        if valor >= 11:

            cartas_fuertes += 1

    return cartas_fuertes >= 1

def decidir_valecuatro(mano):
    """
    La función "decidir_valecuatro" determina si la computadora debe cantar vale cuatro.
    Si la mano contiene un 1 de espada o un 1 de basto (las cartas más fuertes),
    decide cantarlo.
    Retorna True si canta vale cuatro, False en caso contrario.
    """
    cartas_muy_fuertes = 0

    for carta in mano:

        valor = valor_truco(carta[0], carta[1])

        if valor >= 13:

            cartas_muy_fuertes += 1

    return cartas_muy_fuertes >= 1

def hay_ganador(marcador, limite):
    """
    Verifica si alguien ganó
    la partida.
    """
    if marcador["jugador"] >= limite:

        return "Jugador"

    elif marcador["pc"] >= limite:

        return "PC"

    return None
        
def preguntar_si_no(mensaje):
    """
    Pide una respuesta válida: s o si  o n o no
    """
    while True:

        try:

            respuesta = input(mensaje).strip().lower()

            if respuesta == "s" or respuesta == "si" or respuesta == "n" or respuesta == "no":
                return respuesta

            print("Error. Ingresá solamente 's/si'o'n/no'.")

        except Exception:

            print("Ocurrió un error al ingresar la respuesta.")

def preparar_mano():
    """Se le asigna las cartas al jugador y a la pc """

    mazo = crear_mazo()

    mano_pc, mano_jugador = repartir(mazo)

    return mano_pc, mano_jugador

def mostrar_inicio_mano(mano_jugador, mano):
    """En la funcion se muestra las cartas del jugador al inicio de una mano """

    print("\n===== NUEVA MANO =====")

    mostrar_mano(mano_jugador)

    print("\nEmpieza:", mano)

def resolver_envido(mano_jugador,mano_pc,marcador,mano):
    """En esta funcion se hace el calculo del envido en las cartas de la pc y el jugador"""

    envido_pc = calcular_envido(mano_pc)

    envido_jugador = calcular_envido(mano_jugador)

    print("\nTus puntos:", envido_jugador)
    print("Puntos PC:", envido_pc)

    if envido_jugador > envido_pc:

        print("Ganaste el envido.")
        marcador["jugador"] += 2

    elif envido_pc > envido_jugador:

        print("La PC ganó el envido.")
        marcador["pc"] += 2

    else:

        print("Empate de envido.")

        if mano == "jugador":

            print("Ganás por ser mano.")
            marcador["jugador"] += 2

        else:

            print("La PC gana por ser mano.")
            marcador["pc"] += 2

def jugar_envido(mano, mano_pc, mano_jugador, marcador):
    """En esta funcion se decide si la profe canta o no envido y si acepta o no envido """

    if mano == "jugador":

        respuesta = preguntar_si_no(
            "\n¿Querés cantar ENVIDO? (s/si o n/no): "
        )

        if respuesta == "s" or respuesta == "si":

            resolver_envido(
                mano_jugador,
                mano_pc,
                marcador,
                "jugador"
            )

    else:

        if decidir_envido(mano_pc):

            print("\nLa PC canta ENVIDO")

            respuesta = preguntar_si_no(
                "¿Aceptás? (s/si o n/no): "
            )

            if respuesta == "n" or respuesta == "no":

                print("No aceptaste el envido.")
                marcador["pc"] += 1

            else:

                resolver_envido(
                    mano_jugador,
                    mano_pc,
                    marcador,
                    "pc"
                )

def manejar_vale_cuatro_pc(
    mano_pc,
    marcador,
    puntos_truco,
    nivel_truco
):
    """
    Maneja el vale cuatro de la PC.
    """

    try:

        if decidir_valecuatro(mano_pc):

            print("\nLa PC canta VALE CUATRO")

            respuesta = preguntar_si_no(
                "¿Aceptás? (s/si o n/no): "
            )

            if respuesta == "n" or respuesta == "no":

                print("No aceptaste el vale cuatro.")

                marcador["pc"] += 3

                return True, puntos_truco, nivel_truco

            print("Aceptaste el vale cuatro.")

            nivel_truco = 3
            puntos_truco = 4

        return False, puntos_truco, nivel_truco

    except Exception as error:

        print("Error al manejar vale cuatro.")
        print("Error:", error)

        return True, puntos_truco, nivel_truco

def manejar_vale_cuatro_jugador(
    marcador,
    puntos_truco,
    nivel_truco
):
    """
    Permite al jugador cantar vale cuatro.
    """

    try:

        respuesta = preguntar_si_no(
            "¿Querés cantar VALE CUATRO? (s/si o n/no): "
        )

        if respuesta == "s" or respuesta == "si":

            respuesta_pc = random.choice(["s", "n"])

            if respuesta_pc == "n":

                print("La PC no aceptó el vale cuatro.")

                marcador["jugador"] += 3

                return True, puntos_truco, nivel_truco

            print("La PC aceptó el vale cuatro.")

            nivel_truco = 3
            puntos_truco = 4

        return False, puntos_truco, nivel_truco

    except Exception as error:

        print("Error al manejar vale cuatro.")
        print("Error:", error)

        return True, puntos_truco, nivel_truco

def manejar_retruco_jugador(
    mano_pc,
    marcador,
    puntos_truco,
    nivel_truco
):
    """
    Permite al jugador cantar retruco.
    """

    try:

        respuesta = preguntar_si_no(
            "¿Querés cantar RETRUCO? (s/si o n/no): "
        )

        if respuesta == "s" or respuesta == "si":

            respuesta_pc = random.choice(["s", "n"])

            if respuesta_pc == "n":

                print("La PC no aceptó el retruco.")

                marcador["jugador"] += 2

                return True, puntos_truco, nivel_truco

            print("La PC aceptó el retruco.")

            nivel_truco = 2
            puntos_truco = 3

            terminar, puntos_truco, nivel_truco = manejar_vale_cuatro_pc(
                mano_pc,
                marcador,
                puntos_truco,
                nivel_truco
            )

            if terminar:

                return True, puntos_truco, nivel_truco

        return False, puntos_truco, nivel_truco

    except Exception as error:

        print("Error al manejar retruco.")
        print("Error:", error)

        return True, puntos_truco, nivel_truco

def manejar_retruco_pc(
    mano_pc,
    marcador,
    puntos_truco,
    nivel_truco
):
    """
    Permite a la PC cantar retruco
    cuando tiene una mano fuerte.
    """

    try:

        if decidir_retruco(mano_pc):

            print("\nLa PC canta RETRUCO")

            respuesta = preguntar_si_no(
                "¿Aceptás? (s/si o n/no): "
            )

            if respuesta == "n" or respuesta == "no":

                print("No aceptaste el retruco.")

                marcador["pc"] += 2

                return True, puntos_truco, nivel_truco

            print("Aceptaste el retruco.")

            nivel_truco = 2
            puntos_truco = 3

            terminar, puntos_truco, nivel_truco = manejar_vale_cuatro_jugador(
                marcador,
                puntos_truco,
                nivel_truco
            )

            if terminar:

                return True, puntos_truco, nivel_truco

        return False, puntos_truco, nivel_truco

    except Exception as error:

        print("Error al manejar retruco.")
        print("Error:", error)

        return True, puntos_truco, nivel_truco

def manejar_truco(
    turno,
    mano_pc,
    mano_jugador,
    marcador,
    puntos_truco,
    nivel_truco
):
    """
    Maneja las apuestas de truco,
    retruco y vale cuatro.
    """

    try:

        if turno == "pc":

            if nivel_truco == 0 and decidir_truco(mano_pc):

                print("\nLa PC canta TRUCO")

                mostrar_mano(mano_jugador)

                respuesta = preguntar_si_no(
                    "¿Aceptás? (s o n): "
                )

                if respuesta == "n" or respuesta == "no":

                    print("No aceptaste el truco.")

                    marcador["pc"] += 1

                    return True, puntos_truco, nivel_truco

                print("Aceptaste el truco.")

                nivel_truco = 1
                puntos_truco = 2

                terminar, puntos_truco, nivel_truco = manejar_retruco_jugador(
                    mano_pc,
                    marcador,
                    puntos_truco,
                    nivel_truco
                )

                if terminar:

                    return True, puntos_truco, nivel_truco

        else:

            if nivel_truco == 0:

                mostrar_mano(mano_jugador)

                respuesta = preguntar_si_no(
                    "\n¿Querés cantar TRUCO? (si/s o n/no): "
                )

                if respuesta == "s" or respuesta == "si":

                    respuesta_pc = random.choice(["s", "n"])

                    if respuesta_pc == "n":

                        print("La PC no aceptó el truco.")

                        marcador["jugador"] += 1

                        return True, puntos_truco, nivel_truco

                    print("La PC aceptó el truco.")

                    nivel_truco = 1
                    puntos_truco = 2

                    terminar, puntos_truco, nivel_truco = manejar_retruco_pc(
                        mano_pc,
                        marcador,
                        puntos_truco,
                        nivel_truco
                    )

                    if terminar:

                        return True, puntos_truco, nivel_truco

        return False, puntos_truco, nivel_truco

    except Exception as error:

        print("Error al manejar el truco.")
        print("Error:", error)

        return True, puntos_truco, nivel_truco

def jugar_rondas(mano_jugador,mano_pc,turno, mano,marcador,puntos_truco,nivel_truco):
    """En la funcion se suma los puntos obtenidos en cada ronda ganada """

    resultados = []

    ganador_mano = None

    for ronda in range(1,4):

        print("\n--- RONDA", ronda, "---")

        terminar,puntos_truco,nivel_truco = manejar_truco(turno,mano_pc,mano_jugador,marcador,puntos_truco,nivel_truco)

        if terminar:
             if turno == "jugador":
                return "jugador", puntos_truco

             return "pc", puntos_truco
            

        ganador = jugar_ronda(mano_jugador,mano_pc,turno)

        if ganador == "mazo":

            return "pc", puntos_truco

        resultados.append(ganador)

        ganador_mano = ganador_mano_terminada(resultados,mano)

        if ganador_mano != None:

            break

        turno = siguiente_turno(
            ganador,
            turno
        )

    return ganador_mano, puntos_truco

def mostrar_resultado_final(ganador_mano, marcador, puntos_truco):
    """Se muestra el resultado final del jugador y de la pc"""

    print("\n===== RESULTADO =====")

    if ganador_mano == "jugador":

        print("Ganaste la mano.")

        marcador["jugador"] += puntos_truco

    else:

        print("La PC ganó la mano.")

        marcador["pc"] += puntos_truco



def jugar_mano(marcador, quien_empieza):

    mano_pc, mano_jugador = preparar_mano()

    puntos_truco = 1
    nivel_truco = 0

    mano = quien_empieza
    turno = mano

    mostrar_inicio_mano(mano_jugador, mano)

    jugar_envido(mano, mano_pc, mano_jugador, marcador)

    ganador_mano, puntos_truco = jugar_rondas(mano_jugador,mano_pc,turno,mano,marcador,puntos_truco,nivel_truco)

    mostrar_resultado_final(ganador_mano,marcador,puntos_truco)
        
def jugar_partida():
    """
    Ejecuta una partida completa.
    """

    marcador = {
        "jugador": 0,
        "pc": 0
    }

    limite = elegirpuntos()

    print("\n===== COMIENZA LA PARTIDA =====")

    quien_empieza = "jugador"
    seguir_jugando = True

    while hay_ganador(marcador, limite) == None and seguir_jugando:
        
        try:

            jugar_mano(marcador, quien_empieza)
            
        except Exception as error:

            print("\nOcurrió un error durante la mano.")
            print("Error:", error)

        # Alterna quién empieza
        if quien_empieza == "jugador":

            quien_empieza = "pc"

        else:

            quien_empieza = "jugador"

        print("\n===== MARCADOR =====")
        print("Jugador:", marcador["jugador"])
        print("PC:", marcador["pc"])

        if hay_ganador(marcador, limite) == None:
            respuesta = preguntar_si_no("¿Queres seguir jugando?(s/si o n/no): ")
            if respuesta == "n" or respuesta == "no":
                seguir_jugando = False

    ganador = hay_ganador(marcador, limite)

    print("\n===== FIN DE LA PARTIDA =====")

    if ganador != None:

        print("Ganador:", ganador)
        guardar_historial(ganador, marcador)
    else:
        print("La partida fue cancelada")


def reglasDeJuego():
    """
    Muestra las reglas del juego.
    """

    opcion = 0

    while opcion != 4:

        print("\n===== REGLAS =====")
        print("1. Ver reglas generales")
        print("2. Ver sistema de puntos")
        print("3. Ver restricciones")
        print("4. Volver al menú")

        try:

            opcion = int(input("Ingrese opción: "))

            if opcion == 1:

                print("\n--- REGLAS GENERALES ---")
                print("- Se juega contra la computadora")
                print("- Se puede jugar a 15 o 30 puntos")
                print("- Hay envido, truco, retruco y vale cuatro")
                print("- Gana quien llegue primero al límite")

            elif opcion == 2:

                print("\n--- SISTEMA DE PUNTOS ---")
                print("- Envido: 2 puntos")
                print("- Truco: 2 puntos")
                print("- Retruco: 3 puntos")
                print("- Vale cuatro: 4 puntos")

            elif opcion == 3:

                print("\n--- RESTRICCIONES ---")
                print("- No se juega flor")
                print("- No hay falta envido")

            elif opcion == 4:

                print("Volviendo al menú...")

            else:

                print("Opción inválida.")

        except ValueError:

            print("Error. Debe ingresar un número.")
            
def guardar_historial(ganador, marcador):
    """
    Guarda el resultado de cada partida
    en un archivo de texto.
    """

    try:

        with open("historial_truco.txt", "a") as archivo:

            archivo.write(
                "Ganador: " + ganador +
                " | Jugador: " + str(marcador["jugador"]) +
                " | PC: " + str(marcador["pc"]) +
                "\n"
            )

    except Exception as error:

        print("No se pudo guardar el historial.")
        print("Error:", error)

def mostrar_historial():
    """
    Muestra el historial de partidas.
    """

    try:

        with open("historial_truco.txt", "r") as archivo:

            print("\n===== HISTORIAL =====")

            contenido = archivo.read()

            if contenido == "":

                print("No hay partidas guardadas.")

            else:

                print(contenido)

    except FileNotFoundError:

        print("\nTodavía no existe historial.")

    except Exception as error:

        print("Ocurrió un error al leer el historial.")
        print("Error:", error)

def menuDeInicio():

    opcion = 0

    while opcion != 4:

        print("\n===== JUEGO DEL TRUCO =====")
        print("1. Jugar")
        print("2. Ver reglas")
        print("3. Historial")
        print("4. Salir")

        try:

            opcion = int(input("Ingrese opción: "))

            if opcion == 1:

                jugar_partida()

            elif opcion == 2:

                reglasDeJuego()

            elif opcion == 3:

                mostrar_historial()

            elif opcion == 4:

                print("Hasta luego.")

            else:

                print("Opción inválida.")

        except ValueError:

            print("Ingresá un número.")
            
        except Exception:
            print("Ocurrió un error inesperado.")

menuDeInicio()