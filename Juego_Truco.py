
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
            elif opcion == "2":
                reglasDeJuego()
            elif opcion == "3":
                print("Mostrando historial...")
            elif opcion == "4":
                print("¡Hasta Luego!")


